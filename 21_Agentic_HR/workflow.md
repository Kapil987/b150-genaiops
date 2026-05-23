# HR Workflow CLI Diagrams

This file explains how requests move inside `10_agentic_ai/4.w_hr_agentic_workflow` in simple language.

The project has 2 big stages:

1. `PDF -> JSON`
2. `Next Workflow -> scoring + email + Zoom`

---

## 1. Full System View

```text
+-------------------+
| Streamlit UI      |
| streamlit_app_v2  |
+---------+---------+
          |
          | 1) Upload JD PDF + resume PDFs
          | 2) Choose interview slot
          v
+-------------------+
| FastAPI backend   |
| api/main.py       |
+---------+---------+
          |
          | POST /v1/jobs
          v
+-------------------+
| PDF parsing flow  |
| Bedrock + pypdf   |
+---------+---------+
          |
          | returns parsed JSON
          v
+------------------------------+
| Parsed payload               |
| {                            |
|   job_spec,                  |
|   candidates_input           |
| }                            |
+---------------+--------------+
                |
                | POST /v1/next/oneshot
                | or
                | POST /v1/next/hitl/start
                v
+------------------------------+
| Next workflow router         |
| api/nextflow/router.py       |
+---------------+--------------+
                |
                | score candidates by skill match
                v
+----------------------------------------------+
| Candidate buckets                            |
| selected | manual_review | rejected          |
+---------------+------------------------------+
                |
                | run agent actions
                v
+----------------------------------------------+
| Agent + providers                            |
| Groq agent -> Zoom provider -> Email provider|
+---------------+------------------------------+
                |
                v
+----------------------------------------------+
| Final response                               |
| summary, selected, rejected, email_results   |
+----------------------------------------------+
```

---

## 2. PDF To JSON Flow

### What user sends

```text
User/UI
  |
  +-- jd_pdf            -> exactly 1 PDF
  +-- resumes           -> 1 or more PDFs
```

### What backend does

```text
POST /v1/jobs
  |
  +-- validate files
  |    - JD must be PDF
  |    - at least one resume required
  |    - every resume must be PDF
  |
  +-- create job_id
  |
  +-- start async background task: run_job(...)
  |
  +-- return immediately:
       { job_id, status: "running" }
```

### Background parsing flow

```text
run_job(job_id, jd_bytes, resumes)
  |
  +-- extract JD text using pypdf
  |
  +-- parse JD with BedrockJsonClient
  |    output shape:
  |    {
  |      job_id,
  |      title,
  |      required_skills,
  |      min_experience,
  |      max_budget,
  |      location,
  |      match_thresholds
  |    }
  |
  +-- for each resume
  |    |
  |    +-- extract text using pypdf
  |    +-- parse resume with BedrockJsonClient
  |    +-- normalize skills
  |
  +-- save final result:
       {
         job_spec: {...},
         candidates_input: [...]
       }
```

### How UI reads the result

```text
POST /v1/jobs
  -> get job_id

GET /v1/jobs/{job_id}/status
  -> running/completed/failed
  -> recent logs

GET /v1/jobs/{job_id}/result
  -> final parsed JSON
```

### Expected JSON after parsing

```json
{
  "job_spec": {
    "job_id": "JOB-001",
    "title": "ML Engineer",
    "required_skills": ["python", "docker", "bedrock"],
    "min_experience": 3,
    "max_budget": 2500000,
    "location": "Bangalore",
    "match_thresholds": {
      "shortlist_min_percent": 80,
      "reject_max_percent": 50
    }
  },
  "candidates_input": [
    {
      "candidate_id": "CAND-101",
      "name": "Candidate Name",
      "email": "candidate@example.com",
      "skills": ["python", "docker"],
      "experience_years": 4,
      "salary_expectation": 1800000,
      "work_authorized": true
    }
  ]
}
```

---

## 3. Candidate Scoring Flow

This starts after parsed JSON is ready.

```text
Workflow input
  |
  +-- data.job_spec
  +-- data.candidates_input
  +-- slot_start_ist
  +-- slot_end_ist
  v
prepare_scored_lists(...)
  |
  +-- read thresholds from job_spec
  |    shortlist_min_percent default = 80
  |    reject_max_percent default   = 50
  |
  +-- calculate match_percent for each candidate
  |    based on required_skills vs candidate skills
  |
  +-- classify each candidate:
       if match >= shortlist_min      -> selected
       if match <= reject_max         -> rejected
       otherwise                      -> manual_review
```

### Simple decision view

```text
                  +----------------------+
                  | candidate match %    |
                  +----------+-----------+
                             |
          +------------------+------------------+
          |                                     |
   >= shortlist_min                      <= reject_max
          |                                     |
          v                                     v
     SELECTED                               REJECTED
          |
          |
   between both thresholds
          |
          v
     MANUAL REVIEW
```

---

## 4. One-Shot Flow

In one-shot mode, manual-review candidates are auto-approved.

```text
POST /v1/next/oneshot
  |
  +-- score all candidates
  |
  +-- selected      -> final_decision = selected
  +-- manual_review -> final_decision = selected
  +-- rejected      -> final_decision = rejected
  |
  +-- run_agent_actions(all_rows, slot_start_ist, slot_end_ist, job_spec)
  |
  +-- return
       - summary
       - selected[]
       - rejected[]
       - email_results[]
```

### One-shot branch behavior

```text
Candidate
  |
  +-- final_decision = selected?
        |
        +-- YES
        |    +-- allocate 30-min interview slot
        |    +-- create Zoom meeting
        |    +-- send selection email with Zoom link
        |
        +-- NO
             +-- do not create Zoom meeting
             +-- send rejection email
```

---

## 5. HITL Flow

HITL = Human In The Loop.

In this mode, only the middle bucket waits for human approval.

```text
POST /v1/next/hitl/start
  |
  +-- score all candidates
  +-- create run_id
  +-- store shortlisted, rejected, manual_review
  |
  +-- return:
       run_id
       shortlisted[]
       rejected[]
       manual_review[]
```

### Human decision loop

```text
manual_review candidate
  |
  +-- user chooses:
       - approve
       - reject
  |
  +-- POST /v1/next/hitl/decision
       {
         run_id,
         candidate_id,
         decision
       }
```

### Finalize step

```text
POST /v1/next/hitl/finalize
  |
  +-- shortlisted candidates -> selected
  +-- rejected candidates    -> rejected
  +-- manual_review candidates:
       approve -> selected
       reject  -> rejected
  |
  +-- run_agent_actions(...)
  |
  +-- return final summary, selected, rejected, email_results
```

---

## 6. Agent + Tool Flow

This is the most important runtime behavior after decisions are made.

```text
run_agent_actions(candidates, slot_start_ist, slot_end_ist, job_spec)
  |
  +-- build Groq LLM
  |
  +-- for each candidate
       |
       +-- if selected
       |    +-- assign unique 30-min slot
       |
       +-- run tool-calling agent
            |
            +-- tool 1: create_zoom_meeting(...)
            |    only for selected candidates
            |
            +-- tool 2: send_candidate_email(...)
                 must be called exactly once
```

### Internal rule enforced by code

```text
selected candidate
  -> Zoom first
  -> then email

rejected candidate
  -> no Zoom
  -> email only

if send_candidate_email is never called
  -> workflow fails with RuntimeError
```

---

## 7. Provider Flow

```text
Selected candidate
  |
  +-- get Zoom token
  +-- create Zoom meeting
  +-- build interview email body
  +-- send email via Brevo

Rejected candidate
  |
  +-- build rejection email body
  +-- send email via Brevo
```

### Actual provider files

```text
Zoom:
  integrations/zoom_provider.py

Email:
  integrations/email_provider_service.py

Provider wrapper logic:
  api/nextflow/providers.py
```

---

## 8. Important Inputs And Outputs

### Inputs expected by next workflow

```json
{
  "data": {
    "job_spec": {},
    "candidates_input": []
  },
  "slot_start_ist": "14:00",
  "slot_end_ist": "18:00"
}
```

### Output from one-shot/finalize

```json
{
  "summary": {},
  "selected": [],
  "rejected": [],
  "email_results": []
}
```

### Meaning of `email_results`

Each row usually contains:

```text
candidate_id
candidate_name
email
final_decision
send_status
agent_output
meeting            <- only for selected candidates
meeting_source     <- only for selected candidates
```

---

## 9. Failure Points To Remember

```text
PDF stage can fail when:
  - JD is not a PDF
  - resumes are missing
  - resume file is not a PDF
  - Bedrock extraction/parsing fails

Next workflow can fail when:
  - GROQ_API_KEY is missing
  - selected candidates do not fit in the time window
  - Zoom token/credentials are missing for selected candidates
  - send_candidate_email tool is not called by the agent
```

---

## 10. Code Map

If you want to trace the flow quickly, start here:

- UI entry: `streamlit_app_v2.py`
- PDF API: `api/main.py`
- Next workflow routes: `api/nextflow/router.py`
- Scoring logic: `api/nextflow/scoring.py`
- Agent runtime: `api/nextflow/agent_runner.py`
- Email and Zoom wrapper logic: `api/nextflow/providers.py`
- Real provider calls: `integrations/email_provider_service.py`, `integrations/zoom_provider.py`

