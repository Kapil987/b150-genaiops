from __future__ import annotations

import os
from datetime import timedelta
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from .providers import verified_send_for_candidate, zoom_create_with_provider
from .scheduling import interview_datetime_ist


def enable_langsmith_defaults() -> None:
    if os.getenv("LANGSMITH_API_KEY"):
        os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
        os.environ.setdefault("LANGCHAIN_PROJECT", "normal-workflow-poc")
    else:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"


def build_llm(slot_start_ist: str, slot_end_ist: str) -> ChatGroq:
    _ = (slot_start_ist, slot_end_ist)  # kept for interface parity
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is missing.")

    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    return ChatGroq(model=model, temperature=0)


def safe_message_text(agent_output: Any) -> str:
    if hasattr(agent_output, "content"):
        return str(agent_output.content)
    if isinstance(agent_output, dict):
        messages = agent_output.get("messages")
        if isinstance(messages, list) and messages:
            last = messages[-1]
            if hasattr(last, "content"):
                return str(last.content)
            if isinstance(last, dict):
                if "content" in last:
                    return str(last.get("content"))
                return str(last)
        if "output" in agent_output:
            return str(agent_output.get("output"))
    return str(agent_output)


def allocate_slot_for_selected_candidate(
    base_slot_start_ist: str,
    base_slot_end_ist: str,
    selected_index: int,
) -> tuple[str, str]:
    window_start = interview_datetime_ist(base_slot_start_ist)
    window_end = interview_datetime_ist(base_slot_end_ist)

    candidate_start = window_start + timedelta(minutes=30 * selected_index)
    candidate_end = candidate_start + timedelta(minutes=30)
    if candidate_end > window_end:
        raise RuntimeError(
            "Interview slot window is too short for the number of selected candidates at 30-minute intervals."
        )
    return candidate_start.strftime("%H:%M"), candidate_end.strftime("%H:%M")


def _run_candidate_with_tools(
    llm: ChatGroq,
    candidate: dict[str, Any],
    slot_start_ist: str,
    slot_end_ist: str,
    job_spec: dict[str, Any],
) -> tuple[str, dict[str, Any] | None]:
    @tool
    def create_zoom_meeting(candidate_name: str) -> dict[str, Any]:
        """Create a real Zoom meeting for the candidate."""
        return zoom_create_with_provider(candidate_name, slot_start_ist, slot_end_ist)

    @tool
    def send_candidate_email(
        candidate_id: str,
        candidate_name: str,
        candidate_email: str,
        final_decision: str,
        match_percent: int,
    ) -> dict[str, Any]:
        """Send candidate email using provider templates and return verified send status."""
        cand = {
            "candidate_id": candidate_id,
            "name": candidate_name,
            "email": candidate_email,
            "final_decision": final_decision,
            "match_percent": match_percent,
        }
        return verified_send_for_candidate(cand, slot_start_ist, slot_end_ist, job_spec)

    tools = [create_zoom_meeting, send_candidate_email]
    tool_map = {t.name: t for t in tools}
    llm_tools = llm.bind_tools(tools)

    decision = str(candidate.get("final_decision", "rejected"))
    prompt = (
        "You are HR automation assistant.\n"
        "Use tools to execute operations.\n"
        "Always call send_candidate_email exactly once.\n"
        "Call create_zoom_meeting first only when decision is selected.\n"
        f"Candidate id: {candidate.get('candidate_id', '')}\n"
        f"Candidate name: {candidate.get('name', '')}\n"
        f"Candidate email: {candidate.get('email', '')}\n"
        f"Decision: {decision}\n"
        f"Match percent: {int(candidate.get('match_percent', 0) or 0)}\n"
        f"Interview slot IST: {slot_start_ist} to {slot_end_ist}\n"
        "After tool calls, return a short summary."
    )

    messages: list[Any] = [
        SystemMessage(content="Execute tools carefully and return concise status."),
        HumanMessage(content=prompt),
    ]
    verified_payload: dict[str, Any] | None = None

    for _ in range(4):
        ai_msg = llm_tools.invoke(messages)
        messages.append(ai_msg)
        tool_calls = getattr(ai_msg, "tool_calls", None) or []
        if not tool_calls:
            return safe_message_text(ai_msg), verified_payload

        for tc in tool_calls:
            name = tc.get("name", "")
            args = tc.get("args", {}) or {}
            call_id = tc.get("id", "")
            tool_obj = tool_map.get(name)
            if not tool_obj:
                tool_result = {"error": f"Unknown tool: {name}"}
            else:
                try:
                    tool_result = tool_obj.invoke(args)
                    if name == "send_candidate_email" and isinstance(tool_result, dict):
                        verified_payload = tool_result
                except Exception as exc:
                    tool_result = {"error": f"{type(exc).__name__}: {exc}"}
            messages.append(ToolMessage(content=str(tool_result), tool_call_id=call_id))

    return "Tool loop reached max iterations.", verified_payload


def run_agent_actions(
    candidates: list[dict[str, Any]],
    slot_start_ist: str,
    slot_end_ist: str,
    job_spec: dict[str, Any],
) -> list[dict[str, Any]]:
    enable_langsmith_defaults()
    llm = build_llm(slot_start_ist, slot_end_ist)

    results: list[dict[str, Any]] = []
    selected_index = 0
    for c in candidates:
        current_slot_start = slot_start_ist
        current_slot_end = slot_end_ist
        if str(c.get("final_decision", "")).lower() == "selected":
            current_slot_start, current_slot_end = allocate_slot_for_selected_candidate(
                base_slot_start_ist=slot_start_ist,
                base_slot_end_ist=slot_end_ist,
                selected_index=selected_index,
            )
            selected_index += 1

        agent_text, verified = _run_candidate_with_tools(
            llm=llm,
            candidate=c,
            slot_start_ist=current_slot_start,
            slot_end_ist=current_slot_end,
            job_spec=job_spec,
        )
        if verified is None:
            raise RuntimeError(
                f"Tool execution incomplete for candidate {c.get('candidate_id', '')}: "
                "send_candidate_email tool was not called."
            )
        results.append({**verified, "agent_output": agent_text})
    return results
