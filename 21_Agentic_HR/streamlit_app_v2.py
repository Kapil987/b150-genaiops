from __future__ import annotations

import concurrent.futures
import json
import os
import time
from typing import Any

import requests
import streamlit as st


st.set_page_config(page_title="Agentic HR Workflow v2", layout="wide")


def inject_css() -> None:
    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

          :root {
            --bg-a: #0b1020;
            --bg-b: #111a2e;
            --ink: #e8eefc;
            --muted: #a9b8d6;
            --line: #2a3550;
            --active: #ff9f43;
            --ok: #34d399;
            --bad: #fb7185;
            --card: #121a2f;
            --chip: #1a2440;
          }

          .stApp {
            font-family: "Space Grotesk", sans-serif;
            background: radial-gradient(1200px 480px at 2% 2%, #1a2645 0%, transparent 55%),
                        radial-gradient(1000px 400px at 98% 0%, #2d1f2f 0%, transparent 50%),
                        linear-gradient(160deg, var(--bg-a), var(--bg-b));
          }

          .v2-title {
            font-size: 2rem;
            font-weight: 700;
            color: var(--ink);
            margin-bottom: 0.2rem;
          }

          .v2-subtitle {
            color: var(--muted);
            margin-bottom: 1rem;
          }

          .v2-card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 0.8rem 1rem;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
            margin-bottom: 0.75rem;
          }

          [data-testid="stFileUploader"] {
            background: #121b31;
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 0.5rem;
          }

          [data-testid="stFileUploader"] small,
          [data-testid="stFileUploader"] span,
          [data-testid="stFileUploader"] label,
          [data-testid="stFileUploader"] div {
            color: #e8eefc !important;
          }

          [data-baseweb="input"] > div,
          [data-baseweb="select"] > div,
          textarea {
            background: #0f172a !important;
            color: #e8eefc !important;
            border: 1px solid #34425f !important;
          }

          .stButton > button {
            background: linear-gradient(135deg, #ff6f3c, #ff3b3f) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
          }

          .stButton > button:hover {
            filter: brightness(1.05);
          }

          [data-baseweb="tab-list"] {
            gap: 0.4rem;
          }

          [data-baseweb="tab"] {
            color: #bcd0f2 !important;
            background: #131c33 !important;
            border: 1px solid #2d3a57 !important;
            border-radius: 10px 10px 0 0 !important;
            padding: 0.45rem 0.75rem !important;
          }

          [aria-selected="true"][data-baseweb="tab"] {
            color: #f3f7ff !important;
            background: #1a2645 !important;
            border-bottom: 2px solid #ff6f3c !important;
          }

          .cp-wrap {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            overflow-x: auto;
            padding-bottom: 0.2rem;
          }

          .cp-node {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            white-space: nowrap;
            color: var(--muted);
            font-size: 0.84rem;
          }

          .cp-dot {
            width: 22px;
            height: 22px;
            border-radius: 999px;
            border: 2px solid var(--line);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-family: "IBM Plex Mono", monospace;
            font-size: 0.72rem;
            background: #fff;
            color: #cbd8f2;
          }

          .cp-node.done .cp-dot {
            border-color: var(--ok);
            background: #e8f7ef;
            color: var(--ok);
          }

          .cp-node.active .cp-dot {
            border-color: var(--active);
            background: #fff4ea;
            color: var(--active);
          }

          .cp-node.fail .cp-dot {
            border-color: var(--bad);
            background: #ffecee;
            color: var(--bad);
          }

          .cp-line {
            width: 44px;
            border-top: 2px solid var(--line);
            opacity: 0.9;
          }

          .cp-line.done {
            border-color: var(--ok);
          }

          .chip {
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 999px;
            background: var(--chip);
            border: 1px solid #30415f;
            font-size: 0.75rem;
            color: #d4e2ff;
            margin-right: 0.35rem;
          }

          .file-list {
            margin-top: 0.6rem;
            padding: 0.65rem;
            border-radius: 10px;
            border: 1px solid #2f3e5c;
            background: #0f172a;
          }

          .file-item {
            font-family: "IBM Plex Mono", monospace;
            font-size: 0.84rem;
            color: #d7e5ff;
            margin: 0.2rem 0;
          }

          .v2-action-gap {
            height: 10px;
          }

          .v2-action-row {
            margin-top: 2px;
            margin-bottom: 2px;
          }

          .agent-panel {
            background: linear-gradient(160deg, #101b34, #182947);
            color: #f1f6ff;
            border-radius: 14px;
            padding: 0.9rem 1rem;
            border: 1px solid #2d436d;
            box-shadow: 0 12px 26px rgba(5, 16, 33, 0.25);
            margin-bottom: 0.8rem;
          }

          .agent-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-weight: 700;
            margin-bottom: 0.4rem;
          }

          .pulse-wrap {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
          }

          .pulse {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: #4ade80;
            animation: pulse 1.15s infinite ease-in-out;
          }

          .pulse.p2 { animation-delay: 0.15s; }
          .pulse.p3 { animation-delay: 0.3s; }

          @keyframes pulse {
            0%, 100% { opacity: 0.35; transform: translateY(0); }
            50% { opacity: 1; transform: translateY(-2px); }
          }

          .agent-row {
            font-size: 0.82rem;
            color: #d7e5ff;
            margin: 0.18rem 0;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    defaults: dict[str, Any] = {
        "v2_parse_stage": 0,
        "v2_parse_failed": False,
        "v2_parse_logs": [],
        "v2_last_job_id": "",
        "v2_parsed_json": {"job_spec": {}, "candidates_input": []},
        "v2_next_stage": 0,
        "v2_next_failed": False,
        "v2_next_logs": [],
        "v2_hitl_run_id": "",
        "v2_hitl_manual": [],
        "v2_hitl_status_payload": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_checkpoint_bar(
    steps: list[str], current: int, failed: bool = False, container: Any | None = None
) -> None:
    html: list[str] = ['<div class="v2-card"><div class="cp-wrap">']
    last = len(steps) - 1
    for idx, step in enumerate(steps):
        cls = "cp-node"
        if failed and idx == current:
            cls += " fail"
        elif idx < current:
            cls += " done"
        elif idx == current:
            cls += " active"
        dot = "!"
        if not (failed and idx == current):
            dot = "v" if idx < current else str(idx + 1)
        html.append(f'<div class="{cls}"><span class="cp-dot">{dot}</span><span>{step}</span></div>')
        if idx < last:
            line_cls = "cp-line done" if idx < current else "cp-line"
            html.append(f'<div class="{line_cls}"></div>')
    html.append("</div></div>")
    target = container if container is not None else st
    target.markdown("".join(html), unsafe_allow_html=True)


def run_post_with_visual_progress(
    url: str,
    payload: dict[str, Any],
    timeout: int,
    steps: list[str],
    checkpoint_box: Any,
    status_box: Any,
    log_key: str,
    task_label: str,
) -> dict[str, Any]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        fut = pool.submit(requests.post, url, json=payload, timeout=timeout)
        st.session_state[log_key] = [f"Agent grabbed task: {task_label}"]
        tick = 0
        while not fut.done():
            # UI-only progress states while backend request is running.
            stage = 1 if tick < 2 else 2 if tick < 6 else 3
            render_checkpoint_bar(steps, current=stage, failed=False, container=checkpoint_box)
            status_box.info(f"Progress: {steps[stage]}")
            if stage == 1:
                msg = "Agent validated request and submitted workflow."
            elif stage == 2:
                msg = "Agent is working on candidate decisions and tool actions."
            else:
                msg = "Agent is dispatching final actions and preparing response."
            st.session_state[log_key] = [
                st.session_state[log_key][0],
                msg,
                f"Heartbeat tick: {tick + 1}",
            ]
            time.sleep(0.6)
            tick += 1

        resp = fut.result()
        resp.raise_for_status()
        render_checkpoint_bar(steps, current=min(len(steps) - 1, 4), failed=False, container=checkpoint_box)
        status_box.success("Completed")
        st.session_state[log_key] = [
            st.session_state[log_key][0],
            "Agent finished execution.",
            f"Task completed: {task_label}",
        ]
        return resp.json()


def submit_job(backend_url: str) -> str:
    jd_file = st.session_state.get("v2_jd_file")
    resume_files = st.session_state.get("v2_resume_files")
    if not jd_file:
        raise ValueError("Upload JD PDF first.")
    if not resume_files:
        raise ValueError("Upload at least one resume PDF.")

    files = [("jd_pdf", (jd_file.name, jd_file.getvalue(), "application/pdf"))]
    for r in resume_files:
        files.append(("resumes", (r.name, r.getvalue(), "application/pdf")))

    resp = requests.post(f"{backend_url}/v1/jobs", files=files, timeout=120)
    resp.raise_for_status()
    return resp.json()["job_id"]


def poll_job(
    backend_url: str,
    job_id: str,
    steps: list[str],
    checkpoint_box: Any,
) -> dict[str, Any]:
    status_box = st.empty()
    log_box = st.empty()
    bar = st.progress(0)

    for i in range(600):
        s = requests.get(f"{backend_url}/v1/jobs/{job_id}/status", timeout=60)
        s.raise_for_status()
        data = s.json()
        logs = data.get("logs", [])
        st.session_state["v2_parse_logs"] = logs
        latest = logs[-1] if logs else "Waiting..."
        status_box.info(f"Status: {data['status']} | {latest}")
        log_box.code("\n".join(logs[-8:]) if logs else "No logs yet.")
        bar.progress(min(int((i + 1) / 600 * 100), 95))
        # While backend is running, show "Parsing" as active checkpoint.
        render_checkpoint_bar(steps, current=2, failed=False, container=checkpoint_box)

        if data["status"] in {"completed", "failed"}:
            break
        time.sleep(1)

    r = requests.get(f"{backend_url}/v1/jobs/{job_id}/result", timeout=60)
    r.raise_for_status()
    bar.progress(100)
    final = r.json()
    if final.get("status") == "completed":
        render_checkpoint_bar(steps, current=3, failed=False, container=checkpoint_box)
    else:
        render_checkpoint_bar(steps, current=2, failed=True, container=checkpoint_box)
    return final


def show_summary_chips(parsed: dict[str, Any]) -> None:
    job = parsed.get("job_spec", {}) if isinstance(parsed, dict) else {}
    candidates = parsed.get("candidates_input", []) if isinstance(parsed, dict) else []
    required = job.get("required_skills", []) if isinstance(job, dict) else []
    if not isinstance(required, list):
        required = []
    if not isinstance(candidates, list):
        candidates = []
    st.markdown(
        f"""
        <div class="v2-card">
          <span class="chip">Candidates: {len(candidates)}</span>
          <span class="chip">Required Skills: {len(required)}</span>
          <span class="chip">Role: {job.get("title", "N/A")}</span>
          <span class="chip">Location: {job.get("location", "N/A")}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_uploaded_files() -> None:
    jd_file = st.session_state.get("v2_jd_file")
    resumes = st.session_state.get("v2_resume_files") or []
    jd_name = jd_file.name if jd_file else "No JD selected"
    rows: list[str] = [f'<div class="file-item">JD: {jd_name}</div>']
    if resumes:
        for f in resumes:
            rows.append(f'<div class="file-item">Resume: {f.name}</div>')
    else:
        rows.append('<div class="file-item">Resume: No files selected</div>')
    st.markdown(f'<div class="file-list">{"".join(rows)}</div>', unsafe_allow_html=True)


def render_agent_panel(stage_name: str, logs: list[str] | None = None, failed: bool = False) -> None:
    if failed:
        state_text = "State: blocked"
        signal = '<span class="pulse" style="background:#ff6b6b;"></span>'
    else:
        state_text = "State: active"
        signal = '<span class="pulse"></span><span class="pulse p2"></span><span class="pulse p3"></span>'
    recent = logs[-2:] if logs else ["Awaiting tasks", "No events yet"]
    st.markdown(
        f"""
        <div class="agent-panel">
          <div class="agent-head">
            <span>Agent Runtime</span>
            <span class="pulse-wrap">{signal}</span>
          </div>
          <div class="agent-row">{state_text}</div>
          <div class="agent-row">Checkpoint: {stage_name}</div>
          <div class="agent-row">Trace 1: {recent[0]}</div>
          <div class="agent-row">Trace 2: {recent[-1]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_email_summary(result: dict[str, Any]) -> None:
    rows = result.get("email_results", []) if isinstance(result, dict) else []
    if not isinstance(rows, list):
        rows = []
    sent = 0
    failed = 0
    for r in rows:
        item = r or {}
        status = item.get("send_status", {}) if isinstance(item, dict) else {}
        ok = bool(status.get("sent", False)) if isinstance(status, dict) else False
        if ok:
            sent += 1
        else:
            failed += 1
    st.markdown(
        f"""
        <div class="v2-card">
          <span class="chip">Email Step</span>
          <span class="chip">Sent: {sent}</span>
          <span class="chip">Failed: {failed}</span>
          <span class="chip">Total: {len(rows)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown('<div class="v2-title">Agentic HR Workflow v2</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="v2-subtitle">Pipeline checkpoints + higher-clarity operations UI. Backend APIs unchanged.</div>',
        unsafe_allow_html=True,
    )


inject_css()
init_state()
render_header()

backend_url = st.text_input("FastAPI URL", os.getenv("BACKEND_URL", "http://localhost:8000"))
tab_parse, tab_next = st.tabs(["1) PDF -> JSON (v2)", "2) Next Workflow (v2)"])


with tab_parse:
    parse_steps = ["Upload", "Submitted", "Parsing", "Result Ready"]
    parse_checkpoint = st.empty()
    render_checkpoint_bar(
        parse_steps,
        current=st.session_state["v2_parse_stage"],
        failed=st.session_state["v2_parse_failed"],
        container=parse_checkpoint,
    )

    left, right = st.columns([1.25, 1], gap="large")
    with left:
        st.markdown('<div class="v2-card">', unsafe_allow_html=True)
        st.subheader("Upload PDFs")
        st.session_state["v2_jd_file"] = st.file_uploader(
            "Job Description PDF",
            type=["pdf"],
            accept_multiple_files=False,
            key="v2_jd_file_uploader",
        )
        st.session_state["v2_resume_files"] = st.file_uploader(
            "Resume PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            key="v2_resume_files_uploader",
        )
        render_uploaded_files()
        st.markdown('<div class="v2-action-gap"></div>', unsafe_allow_html=True)
        st.markdown('<div class="v2-action-row"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1], gap="medium")
        with c1:
            run_parse = st.button("Run Parse Pipeline", type="primary", key="v2_process_pdfs_btn")
        with c2:
            reset_parse = st.button("Reset Parse State", key="v2_reset_parse_btn")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        parse_stage_name = parse_steps[min(st.session_state["v2_parse_stage"], len(parse_steps) - 1)]
        render_agent_panel(
            parse_stage_name,
            st.session_state.get("v2_parse_logs", []),
            st.session_state["v2_parse_failed"],
        )
        st.markdown('<div class="v2-card">', unsafe_allow_html=True)
        st.subheader("Live Status")
        st.caption("Tracks job state from API logs while parsing resumes.")
        if st.session_state["v2_last_job_id"]:
            st.code(f"job_id: {st.session_state['v2_last_job_id']}")
        else:
            st.code("job_id: <not started>")
        if st.session_state["v2_parse_logs"]:
            st.code("\n".join(st.session_state["v2_parse_logs"][-8:]))
        else:
            st.code("No logs yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    if reset_parse:
        st.session_state["v2_parse_stage"] = 0
        st.session_state["v2_parse_failed"] = False
        st.session_state["v2_parse_logs"] = []
        st.session_state["v2_last_job_id"] = ""
        st.session_state["v2_parsed_json"] = {"job_spec": {}, "candidates_input": []}
        st.rerun()

    if run_parse:
        try:
            st.session_state["v2_parse_failed"] = False
            st.session_state["v2_parse_stage"] = 1
            render_checkpoint_bar(parse_steps, current=1, failed=False, container=parse_checkpoint)
            job_id = submit_job(backend_url)
            st.session_state["v2_last_job_id"] = job_id
            st.session_state["v2_parse_stage"] = 2
            render_checkpoint_bar(parse_steps, current=2, failed=False, container=parse_checkpoint)
            result = poll_job(backend_url, job_id, parse_steps, parse_checkpoint)
            if result["status"] == "completed":
                st.session_state["v2_parse_stage"] = 3
                render_checkpoint_bar(parse_steps, current=3, failed=False, container=parse_checkpoint)
                parsed_json = result.get("result") or {"job_spec": {}, "candidates_input": []}
                st.session_state["v2_parsed_json"] = parsed_json
                st.success("Parsing completed.")
            else:
                st.session_state["v2_parse_failed"] = True
                st.session_state["v2_parse_stage"] = 2
                render_checkpoint_bar(parse_steps, current=2, failed=True, container=parse_checkpoint)
                st.error(result.get("error") or "Parsing failed.")
        except Exception as exc:
            st.session_state["v2_parse_failed"] = True
            st.session_state["v2_parse_stage"] = max(st.session_state["v2_parse_stage"], 1)
            render_checkpoint_bar(
                parse_steps,
                current=st.session_state["v2_parse_stage"],
                failed=True,
                container=parse_checkpoint,
            )
            st.error(str(exc))

    parsed = st.session_state.get("v2_parsed_json", {"job_spec": {}, "candidates_input": []})
    if parsed.get("job_spec") or parsed.get("candidates_input"):
        show_summary_chips(parsed)
        st.download_button(
            "Download Parsed JSON",
            data=json.dumps(parsed, indent=2),
            file_name="combined_output_v2.json",
            mime="application/json",
            key="v2_download_parsed_json",
        )
        with st.expander("View Parsed JSON", expanded=False):
            st.json(parsed)


with tab_next:
    next_steps = ["Input Ready", "Submitted", "Decisioning", "Email Dispatch", "Completed"]
    next_checkpoint = st.empty()
    next_status = st.empty()
    render_checkpoint_bar(
        next_steps,
        current=st.session_state["v2_next_stage"],
        failed=st.session_state["v2_next_failed"],
        container=next_checkpoint,
    )
    next_stage_name = next_steps[min(st.session_state["v2_next_stage"], len(next_steps) - 1)]
    render_agent_panel(
        next_stage_name,
        logs=st.session_state.get("v2_next_logs", []),
        failed=st.session_state["v2_next_failed"],
    )

    st.text_area(
        "Input JSON",
        value=json.dumps(st.session_state.get("v2_parsed_json", {"job_spec": {}, "candidates_input": []}), indent=2),
        height=260,
        key="v2_next_input_json",
    )

    c1, c2, c3 = st.columns([1, 1, 1.2], gap="large")
    with c1:
        st.text_input("IST slot start", value="14:00", key="v2_slot_start")
    with c2:
        st.text_input("IST slot end", value="18:00", key="v2_slot_end")
    with c3:
        mode = st.radio("Mode", ["One-Shot", "HITL"], horizontal=True, key="v2_next_mode")

    def workflow_payload() -> dict[str, Any]:
        return {
            "data": json.loads(st.session_state["v2_next_input_json"]),
            "slot_start_ist": st.session_state["v2_slot_start"],
            "slot_end_ist": st.session_state["v2_slot_end"],
        }

    if mode == "One-Shot":
        if st.button("Run One-Shot Workflow", type="primary", key="v2_run_oneshot"):
            try:
                st.session_state["v2_next_failed"] = False
                st.session_state["v2_next_stage"] = 1
                payload = workflow_payload()
                data = run_post_with_visual_progress(
                    url=f"{backend_url}/v1/next/oneshot",
                    payload=payload,
                    timeout=300,
                    steps=next_steps,
                    checkpoint_box=next_checkpoint,
                    status_box=next_status,
                    log_key="v2_next_logs",
                    task_label="One-Shot Workflow",
                )
                st.session_state["v2_next_stage"] = 4
                show_email_summary(data)
                st.success("One-shot workflow completed.")

                summary = data.get("summary", {})
                m1, m2, m3 = st.columns(3)
                m1.metric("Selected", summary.get("selected_count", 0))
                m2.metric("Rejected", summary.get("rejected_count", 0))
                m3.metric("Manual Auto Approved", summary.get("manual_auto_approved_count", 0))
                show_email_summary(data)
                with st.expander("Result JSON", expanded=False):
                    st.json(data)
            except Exception as exc:
                st.session_state["v2_next_failed"] = True
                st.session_state["v2_next_stage"] = max(st.session_state["v2_next_stage"], 1)
                st.error(str(exc))
    else:
        hitl_steps = ["Input Ready", "Run Started", "Manual Review", "Email Dispatch", "Finalized"]
        hitl_checkpoint = st.empty()
        render_checkpoint_bar(
            hitl_steps,
            current=min(st.session_state["v2_next_stage"], len(hitl_steps) - 1),
            failed=st.session_state["v2_next_failed"],
            container=hitl_checkpoint,
        )

        if st.button("Start HITL Run", type="primary", key="v2_start_hitl"):
            try:
                st.session_state["v2_next_failed"] = False
                st.session_state["v2_next_stage"] = 1
                resp = requests.post(f"{backend_url}/v1/next/hitl/start", json=workflow_payload(), timeout=120)
                resp.raise_for_status()
                data = resp.json()
                st.session_state["v2_hitl_run_id"] = data["run_id"]
                st.session_state["v2_hitl_manual"] = data.get("manual_review", [])
                st.session_state["v2_hitl_status_payload"] = data
                st.session_state["v2_next_stage"] = 2
                st.success(f"HITL started. run_id: {data['run_id']}")
                st.session_state["v2_next_logs"] = [
                    "Agent grabbed task: HITL Run",
                    "Agent created HITL run and queued manual review.",
                    f"Awaiting reviewer decisions for run_id: {data['run_id']}",
                ]
            except Exception as exc:
                st.session_state["v2_next_failed"] = True
                st.error(str(exc))

        run_id = st.session_state.get("v2_hitl_run_id")
        manual = st.session_state.get("v2_hitl_manual", [])
        if run_id:
            st.markdown('<div class="v2-card">', unsafe_allow_html=True)
            st.write(f"Current run_id: `{run_id}`")
            st.markdown("</div>", unsafe_allow_html=True)

            if manual:
                st.subheader("Manual Review Decisions")
                for c in manual:
                    cid = c.get("candidate_id", "")
                    name = c.get("name", "Candidate")
                    match = c.get("match_percent", 0)
                    card = st.container()
                    with card:
                        a, b, d = st.columns([1.6, 1, 0.9])
                        with a:
                            st.write(f"**{name}**  |  `{cid or 'no-id'}`")
                        with b:
                            st.write(f"Match: **{match}%**")
                        with d:
                            choice = st.selectbox(
                                "Decision",
                                ["approve", "reject"],
                                key=f"v2_decision_{cid or name}",
                                label_visibility="collapsed",
                            )
                        if st.button(f"Save decision for {cid or name}", key=f"v2_save_{cid or name}"):
                            try:
                                resp = requests.post(
                                    f"{backend_url}/v1/next/hitl/decision",
                                    json={"run_id": run_id, "candidate_id": cid, "decision": choice},
                                    timeout=60,
                                )
                                resp.raise_for_status()
                                st.success(f"Saved: {cid or name} -> {choice}")
                            except Exception as exc:
                                st.error(str(exc))

            if st.button("Finalize HITL Workflow", key="v2_finalize_hitl"):
                try:
                    data = run_post_with_visual_progress(
                        url=f"{backend_url}/v1/next/hitl/finalize",
                        payload={"run_id": run_id},
                        timeout=300,
                        steps=hitl_steps,
                        checkpoint_box=hitl_checkpoint,
                        status_box=next_status,
                        log_key="v2_next_logs",
                        task_label="HITL Finalize",
                    )
                    st.session_state["v2_next_stage"] = 4
                    show_email_summary(data)
                    st.success("HITL finalize completed.")

                    summary = data.get("summary", {})
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Selected", summary.get("selected_count", 0))
                    m2.metric("Rejected", summary.get("rejected_count", 0))
                    m3.metric("Manual Reviewed", summary.get("manual_review_count", 0))
                    show_email_summary(data)
                    with st.expander("Result JSON", expanded=False):
                        st.json(data)
                except Exception as exc:
                    st.session_state["v2_next_failed"] = True
                    st.error(str(exc))
