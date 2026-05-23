from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class WorkflowInput(BaseModel):
    data: dict[str, Any]
    slot_start_ist: str
    slot_end_ist: str


class OneShotResponse(BaseModel):
    summary: dict[str, Any]
    selected: list[dict[str, Any]]
    rejected: list[dict[str, Any]]
    email_results: list[dict[str, Any]]


class HitlStartResponse(BaseModel):
    run_id: str
    shortlisted: list[dict[str, Any]]
    rejected: list[dict[str, Any]]
    manual_review: list[dict[str, Any]]


class HitlDecisionRequest(BaseModel):
    run_id: str
    candidate_id: str
    decision: Literal["approve", "reject"]


class HitlFinalizeRequest(BaseModel):
    run_id: str

