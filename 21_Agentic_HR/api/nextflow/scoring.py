from __future__ import annotations

import re
from typing import Any


SKILL_ALIASES: dict[str, str] = {
    "amazon sagemaker": "sagemaker",
    "aws sagemaker": "sagemaker",
    "sagemaker": "sagemaker",
    "amazon bedrock": "bedrock",
    "aws bedrock": "bedrock",
    "bedrock": "bedrock",
    "aws lambda": "lambda",
    "amazon lambda": "lambda",
    "lambda": "lambda",
    "amazon s3": "s3",
    "aws s3": "s3",
    "s3": "s3",
    "retrieval-augmented generation": "rag",
    "retrieval augmented generation": "rag",
}


def _normalize_skill(skill: Any) -> str:
    s = str(skill).strip().lower()
    if not s:
        return ""
    s = re.sub(r"\(.*?\)", "", s).strip()
    s = re.sub(r"[^a-z0-9+#.\-/\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return SKILL_ALIASES.get(s, s)


def _skills_match(required: str, candidate: str) -> bool:
    if required == candidate:
        return True
    if required and candidate and (required in candidate or candidate in required):
        return True
    return False


def calc_match_percent(job_spec: dict[str, Any], candidate: dict[str, Any]) -> int:
    required_raw = job_spec.get("required_skills", [])
    skills_raw = candidate.get("skills", [])
    if not isinstance(required_raw, list):
        required_raw = []
    if not isinstance(skills_raw, list):
        skills_raw = []
    required = {_normalize_skill(s) for s in required_raw}
    skills = {_normalize_skill(s) for s in skills_raw}
    required.discard("")
    skills.discard("")
    if not required:
        return 0

    matched_required = 0
    for req in required:
        if any(_skills_match(req, cand) for cand in skills):
            matched_required += 1
    return int((matched_required / len(required)) * 100)


def thresholds(job_spec: dict[str, Any]) -> tuple[int, int]:
    m = job_spec.get("match_thresholds") or {}
    if not isinstance(m, dict):
        m = {}
    try:
        shortlist = int(m.get("shortlist_min_percent", 80))
    except Exception:
        shortlist = 80
    try:
        reject = int(m.get("reject_max_percent", 50))
    except Exception:
        reject = 50
    return shortlist, reject


def classify(job_spec: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    shortlist_min, reject_max = thresholds(job_spec)
    match = calc_match_percent(job_spec, candidate)
    if match >= shortlist_min:
        decision = "selected"
    elif match <= reject_max:
        decision = "rejected"
    else:
        decision = "manual_review"
    return {"decision": decision, "match_percent": match}


def prepare_scored_lists(
    data: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    if not isinstance(data, dict):
        data = {}
    job_spec = data.get("job_spec") or {}
    if not isinstance(job_spec, dict):
        job_spec = {}
    candidates = data.get("candidates_input") or []
    if not isinstance(candidates, list):
        candidates = []

    shortlisted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    manual: list[dict[str, Any]] = []

    for c in candidates:
        if not isinstance(c, dict):
            continue
        row = dict(c)
        cls = classify(job_spec, row)
        row.update(cls)
        if row["decision"] == "selected":
            shortlisted.append(row)
        elif row["decision"] == "rejected":
            rejected.append(row)
        else:
            manual.append(row)

    return job_spec, shortlisted, rejected, manual
