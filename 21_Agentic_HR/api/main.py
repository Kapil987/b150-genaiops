from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from io import BytesIO
import re
from textwrap import dedent
from typing import Any, Literal

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from pydantic import BaseModel

from .bedrock_client import BedrockJsonClient
from .nextflow.router import router as next_workflow_router


class JobCreateResponse(BaseModel):
    job_id: str
    status: Literal["running", "completed", "failed"]


class JobStatusResponse(BaseModel):
    job_id: str
    status: Literal["running", "completed", "failed"]
    logs: list[str]
    error: str | None = None


class JobResultResponse(BaseModel):
    job_id: str
    status: Literal["running", "completed", "failed"]
    result: dict[str, Any] | None = None
    error: str | None = None


@dataclass
class JobState:
    status: Literal["running", "completed", "failed"] = "running"
    logs: list[str] = field(default_factory=list)
    result: dict[str, Any] | None = None
    error: str | None = None


app = FastAPI(title="Simple HR PDF Parser", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)
app.include_router(next_workflow_router)
JOBS: dict[str, JobState] = {}
LOCK = asyncio.Lock()


def extract_pdf_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    return "\n".join((page.extract_text() or "") for page in reader.pages).strip()


def normalize_skills(raw_skills: Any) -> list[str]:
    if not isinstance(raw_skills, list):
        return []

    skip_headings = {
        "skills",
        "mlops & devops",
        "generative ai & llms",
        "cloud platforms (aws)",
        "programming & frameworks",
        "tools & ides",
    }
    tokens: list[str] = []
    for item in raw_skills:
        text = str(item).strip()
        if not text:
            continue

        # Handle lines like "Cloud Platforms (AWS): Amazon SageMaker, AWS Lambda"
        heading_match = re.match(r"^[A-Za-z0-9\s&()/+-]+:\s*(.+)$", text)
        if heading_match:
            text = heading_match.group(1).strip()

        # Split grouped items if model returns comma/pipe/semicolon separated skills.
        parts = re.split(r"[,|;]+", text)
        for part in parts:
            p = part.strip()
            if not p:
                continue
            # Split compact slash pairs like "Git/GitHub" while keeping multi-word terms intact.
            slash_parts = [x.strip() for x in p.split("/") if x.strip()]
            for sp in slash_parts:
                # Remove parenthetical descriptors.
                token = re.sub(r"\(.*?\)", "", sp).strip()
                token = re.sub(r"^[\-\u2022]\s*", "", token).strip()
                p_lower = token.lower()
                # Drop section headings and generic labels.
                if p_lower in skip_headings:
                    continue
                # If line still looks like heading (ends with ':'), drop it.
                if p_lower.endswith(":"):
                    continue
                if not p_lower:
                    continue
                tokens.append(p_lower)

    # Deduplicate, preserve order.
    seen: set[str] = set()
    out: list[str] = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


async def parse_jd(llm: BedrockJsonClient, jd_text: str) -> dict[str, Any]:
    system_prompt = "Extract job description into strict JSON only."
    user_prompt = dedent(
        f"""
        Return JSON with exact schema:
        {{
          "job_id": "JOB-001",
          "title": "",
          "required_skills": [],
          "min_experience": 0,
          "max_budget": 0,
          "location": "",
          "match_thresholds": {{
            "shortlist_min_percent": 80,
            "reject_max_percent": 50
          }}
        }}

        Text:
        {jd_text}
        """
    ).strip()
    return await llm.extract_json(system_prompt, user_prompt)


async def parse_resume(llm: BedrockJsonClient, resume_text: str) -> dict[str, Any]:
    system_prompt = "Extract resume into strict JSON only."
    user_prompt = dedent(
        f"""
        Return JSON with exact schema:
        {{
          "candidate_id": "",
          "name": "",
          "email": "",
          "skills": [],
          "experience_years": 0,
          "salary_expectation": 0,
          "work_authorized": true
        }}

        Rules for "skills":
        - Return atomic skills only, not category headings.
        - Do NOT return section labels like "MLOps & DevOps", "Cloud Platforms (AWS)", "Programming & Frameworks", "Tools & IDEs".
        - Preserve compound vendor-qualified skills exactly when present, e.g. "amazon sagemaker", "amazon bedrock", "aws lambda", "amazon s3".
        - Extract concrete technologies such as: langchain, bedrock, rag, mlflow, kubernetes, kserve, docker, dvc, python, flask, git, amazon sagemaker.
        - Skills should be lowercase where possible.

        Text:
        {resume_text}
        """
    ).strip()
    return await llm.extract_json(system_prompt, user_prompt)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/jobs", response_model=JobCreateResponse)
async def create_job(
    jd_pdf: UploadFile = File(...),
    resumes: list[UploadFile] = File(...),
) -> JobCreateResponse:
    if not jd_pdf.filename or not jd_pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="jd_pdf must be a PDF.")
    if not resumes:
        raise HTTPException(status_code=400, detail="At least one resume PDF is required.")
    for resume in resumes:
        if not resume.filename or not resume.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="All resumes must be PDF files.")

    job_id = str(uuid.uuid4())
    state = JobState(status="running")
    state.logs.append(f"Job started with {len(resumes)} resume(s).")
    async with LOCK:
        JOBS[job_id] = state

    jd_bytes = await jd_pdf.read()
    resume_bytes = [(r.filename or "resume.pdf", await r.read()) for r in resumes]
    asyncio.create_task(run_job(job_id, jd_bytes, resume_bytes))
    return JobCreateResponse(job_id=job_id, status=state.status)


@app.get("/v1/jobs/{job_id}/status", response_model=JobStatusResponse)
async def job_status(job_id: str) -> JobStatusResponse:
    state = JOBS.get(job_id)
    if not state:
        raise HTTPException(status_code=404, detail="Unknown job_id.")
    return JobStatusResponse(
        job_id=job_id,
        status=state.status,
        logs=state.logs[-20:],
        error=state.error,
    )


@app.get("/v1/jobs/{job_id}/result", response_model=JobResultResponse)
async def job_result(job_id: str) -> JobResultResponse:
    state = JOBS.get(job_id)
    if not state:
        raise HTTPException(status_code=404, detail="Unknown job_id.")
    return JobResultResponse(job_id=job_id, status=state.status, result=state.result, error=state.error)


async def run_job(
    job_id: str,
    jd_bytes: bytes,
    resumes: list[tuple[str, bytes]],
) -> None:
    state = JOBS[job_id]
    llm = BedrockJsonClient()
    try:
        jd_text = extract_pdf_text(jd_bytes)

        jd_json = await parse_jd(llm, jd_text)

        sem = asyncio.Semaphore(5)

        async def parse_one(filename: str, blob: bytes) -> dict[str, Any]:
            async with sem:
                text = extract_pdf_text(blob)
                data = await parse_resume(llm, text)
                data["skills"] = normalize_skills(data.get("skills", []))
                return data

        parsed = await asyncio.gather(*[parse_one(fn, blob) for fn, blob in resumes])
        state.result = {"job_spec": jd_json, "candidates_input": parsed}
        state.status = "completed"
        state.logs.append("Job completed.")
    except Exception as exc:
        state.status = "failed"
        state.error = str(exc)
        state.logs.append(f"Job failed: {exc}")
