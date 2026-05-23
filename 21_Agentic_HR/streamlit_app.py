from __future__ import annotations

import json
import os
import time
from typing import Any

import requests
import streamlit as st


st.set_page_config(page_title="HR PDF Parser", layout="wide")
st.title("Agentic HR Workflow")
st.caption("Tab 1: Parse PDFs to JSON. Tab 2: Run next workflow (One-Shot or HITL).")

backend_url = st.text_input("FastAPI URL", os.getenv("BACKEND_URL", "http://localhost:8000"))
tab_parse, tab_next = st.tabs(["1) PDF -> JSON", "2) Next Workflow"])


def submit_job() -> str:
    jd_file = st.session_state.get("jd_file")
    resume_files = st.session_state.get("resume_files")
    if not jd_file:
        raise ValueError("Please upload JD PDF.")
    if not resume_files:
        raise ValueError("Please upload at least one resume PDF.")

    files = [("jd_pdf", (jd_file.name, jd_file.getvalue(), "application/pdf"))]
    for r in resume_files:
        files.append(("resumes", (r.name, r.getvalue(), "application/pdf")))

    resp = requests.post(f"{backend_url}/v1/jobs", files=files, timeout=120)
    resp.raise_for_status()
    return resp.json()["job_id"]


def poll(job_id: str) -> dict[str, Any]:
    status_box = st.empty()

    for _ in range(600):
        s = requests.get(f"{backend_url}/v1/jobs/{job_id}/status", timeout=60)
        s.raise_for_status()
        data = s.json()

        logs = data.get("logs", [])
        latest = logs[-1] if logs else "Waiting..."
        status_box.write(f"Status: **{data['status']}** | {latest}")

        if data["status"] in {"completed", "failed"}:
            break
        time.sleep(1)

    r = requests.get(f"{backend_url}/v1/jobs/{job_id}/result", timeout=60)
    r.raise_for_status()
    return r.json()


with tab_parse:
    st.subheader("Upload PDFs")
    st.session_state["jd_file"] = st.file_uploader(
        "Job Description PDF", type=["pdf"], accept_multiple_files=False, key="jd_file_uploader"
    )
    st.session_state["resume_files"] = st.file_uploader(
        "Resume PDFs", type=["pdf"], accept_multiple_files=True, key="resume_files_uploader"
    )

    if st.button("Process PDFs", type="primary", key="process_pdfs_btn"):
        try:
            job_id = submit_job()
            st.info(f"Job submitted: {job_id}")
            result = poll(job_id)
            if result["status"] == "completed":
                st.success("Completed.")
                parsed_json = result["result"]
                st.session_state["parsed_json"] = parsed_json
                st.json(parsed_json)
                st.download_button(
                    "Download JSON",
                    data=json.dumps(parsed_json, indent=2),
                    file_name="combined_output.json",
                    mime="application/json",
                    key="download_parsed_json",
                )
            else:
                st.error(result.get("error") or "Job failed.")
        except Exception as exc:
            st.error(str(exc))


with tab_next:
    st.subheader("Next Workflow")
    default_json = st.session_state.get("parsed_json", {"job_spec": {}, "candidates_input": []})
    input_text = st.text_area(
        "Input JSON (from previous step)",
        value=json.dumps(default_json, indent=2),
        height=280,
        key="next_input_json",
    )
    col1, col2 = st.columns(2)
    with col1:
        slot_start = st.text_input("IST slot start", value="14:00", key="slot_start")
    with col2:
        slot_end = st.text_input("IST slot end", value="18:00", key="slot_end")

    mode = st.selectbox("Mode", ["One-Shot", "HITL"], index=0, key="next_mode")

    def workflow_payload() -> dict[str, Any]:
        return {
            "data": json.loads(st.session_state["next_input_json"]),
            "slot_start_ist": st.session_state["slot_start"],
            "slot_end_ist": st.session_state["slot_end"],
        }

    if mode == "One-Shot":
        if st.button("Run One-Shot Workflow", type="primary", key="run_oneshot"):
            try:
                resp = requests.post(
                    f"{backend_url}/v1/next/oneshot",
                    json=workflow_payload(),
                    timeout=300,
                )
                resp.raise_for_status()
                data = resp.json()
                st.success("One-shot completed.")
                st.json(data)
            except Exception as exc:
                st.error(str(exc))
    else:
        if st.button("Start HITL Run", type="primary", key="start_hitl"):
            try:
                resp = requests.post(
                    f"{backend_url}/v1/next/hitl/start",
                    json=workflow_payload(),
                    timeout=120,
                )
                resp.raise_for_status()
                data = resp.json()
                st.session_state["hitl_run_id"] = data["run_id"]
                st.session_state["hitl_manual"] = data.get("manual_review", [])
                st.session_state["hitl_status_payload"] = data
                st.success(f"HITL run started: {data['run_id']}")
                st.json(data)
            except Exception as exc:
                st.error(str(exc))

        run_id = st.session_state.get("hitl_run_id")
        manual = st.session_state.get("hitl_manual", [])
        if run_id:
            st.write(f"Current run_id: `{run_id}`")
            if manual:
                st.write("Manual Review Decisions")
                for c in manual:
                    cid = c.get("candidate_id", "")
                    name = c.get("name", "")
                    match = c.get("match_percent", 0)
                    key = f"decision_{cid}"
                    choice = st.selectbox(
                        f"{name} ({cid}) - match {match}%",
                        ["approve", "reject"],
                        key=key,
                    )
                    if st.button(f"Save {cid}", key=f"save_{cid}"):
                        try:
                            resp = requests.post(
                                f"{backend_url}/v1/next/hitl/decision",
                                json={
                                    "run_id": run_id,
                                    "candidate_id": cid,
                                    "decision": choice,
                                },
                                timeout=60,
                            )
                            resp.raise_for_status()
                            st.success(f"Saved decision for {cid}: {choice}")
                        except Exception as exc:
                            st.error(str(exc))

            if st.button("Finalize HITL Workflow", key="finalize_hitl"):
                try:
                    resp = requests.post(
                        f"{backend_url}/v1/next/hitl/finalize",
                        json={"run_id": run_id},
                        timeout=300,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    st.success("HITL finalize completed.")
                    st.json(data)
                except Exception as exc:
                    st.error(str(exc))
