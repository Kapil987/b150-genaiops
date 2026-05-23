from __future__ import annotations

import asyncio
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from .agent_runner import run_agent_actions
from .models import (
    HitlDecisionRequest,
    HitlFinalizeRequest,
    HitlStartResponse,
    OneShotResponse,
    WorkflowInput,
)
from .scoring import prepare_scored_lists


router = APIRouter(prefix="/v1/next", tags=["next-workflow"])
HITL_RUNS: dict[str, dict[str, Any]] = {}


@router.post("/oneshot", response_model=OneShotResponse)
async def run_oneshot(payload: WorkflowInput) -> OneShotResponse:
    try:
        job_spec, shortlisted, rejected, manual = prepare_scored_lists(payload.data)
        for c in manual:
            c["final_decision"] = "selected"
        for c in shortlisted:
            c["final_decision"] = "selected"
        for c in rejected:
            c["final_decision"] = "rejected"

        all_rows = shortlisted + manual + rejected
        email_results = await asyncio.to_thread(
            run_agent_actions,
            all_rows,
            payload.slot_start_ist,
            payload.slot_end_ist,
            job_spec,
        )
        return OneShotResponse(
            summary={
                "job_id": job_spec.get("job_id", ""),
                "selected_count": len([x for x in all_rows if x.get("final_decision") == "selected"]),
                "rejected_count": len([x for x in all_rows if x.get("final_decision") == "rejected"]),
                "manual_auto_approved_count": len(manual),
            },
            selected=[x for x in all_rows if x.get("final_decision") == "selected"],
            rejected=[x for x in all_rows if x.get("final_decision") == "rejected"],
            email_results=email_results,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"One-shot failed: {type(exc).__name__}: {exc}") from exc


@router.post("/hitl/start", response_model=HitlStartResponse)
async def start_hitl(payload: WorkflowInput) -> HitlStartResponse:
    job_spec, shortlisted, rejected, manual = prepare_scored_lists(payload.data)
    run_id = str(uuid.uuid4())
    HITL_RUNS[run_id] = {
        "job_spec": job_spec,
        "slot_start_ist": payload.slot_start_ist,
        "slot_end_ist": payload.slot_end_ist,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "manual_review": manual,
        "decisions": {},
    }
    return HitlStartResponse(
        run_id=run_id, shortlisted=shortlisted, rejected=rejected, manual_review=manual
    )


@router.post("/hitl/decision")
async def hitl_decision(payload: HitlDecisionRequest) -> dict[str, Any]:
    run = HITL_RUNS.get(payload.run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run_id not found.")
    run["decisions"][payload.candidate_id] = payload.decision
    return {"run_id": payload.run_id, "saved": True, "decisions": run["decisions"]}


@router.post("/hitl/finalize", response_model=OneShotResponse)
async def hitl_finalize(payload: HitlFinalizeRequest) -> OneShotResponse:
    run = HITL_RUNS.get(payload.run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run_id not found.")

    job_spec = run["job_spec"]
    shortlisted = [dict(x) for x in run["shortlisted"]]
    rejected = [dict(x) for x in run["rejected"]]
    manual = [dict(x) for x in run["manual_review"]]
    decisions: dict[str, str] = run["decisions"]

    for c in shortlisted:
        c["final_decision"] = "selected"
    for c in rejected:
        c["final_decision"] = "rejected"
    for c in manual:
        user_decision = decisions.get(c.get("candidate_id", ""), "reject")
        c["final_decision"] = "selected" if user_decision == "approve" else "rejected"

    all_rows = shortlisted + manual + rejected
    email_results = await asyncio.to_thread(
        run_agent_actions,
        all_rows,
        run["slot_start_ist"],
        run["slot_end_ist"],
        job_spec,
    )
    return OneShotResponse(
        summary={
            "job_id": job_spec.get("job_id", ""),
            "selected_count": len([x for x in all_rows if x.get("final_decision") == "selected"]),
            "rejected_count": len([x for x in all_rows if x.get("final_decision") == "rejected"]),
            "manual_review_count": len(manual),
        },
        selected=[x for x in all_rows if x.get("final_decision") == "selected"],
        rejected=[x for x in all_rows if x.get("final_decision") == "rejected"],
        email_results=email_results,
    )

