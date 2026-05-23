from __future__ import annotations

from typing import Any
from zoneinfo import ZoneInfo

from integrations.email_provider_service import send_email_dynamic
from integrations.zoom_provider import create_zoom_meeting_dynamic, get_zoom_token_dynamic

from .scoring import thresholds
from .scheduling import interview_date_label, interview_datetime_ist


def zoom_create_with_provider(candidate_name: str, slot_start_ist: str, slot_end_ist: str) -> dict[str, Any]:
    token = get_zoom_token_dynamic()
    if not token:
        raise RuntimeError("Zoom credentials/token unavailable.")

    start_dt_ist = interview_datetime_ist(slot_start_ist)
    end_dt_ist = interview_datetime_ist(slot_end_ist)
    duration_min = max(30, int((end_dt_ist - start_dt_ist).total_seconds() / 60))
    meeting = create_zoom_meeting_dynamic(
        token=token,
        topic=f"Interview - {candidate_name}",
        start_time_iso=start_dt_ist.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ"),
        duration_minutes=duration_min,
        timezone_name="Asia/Kolkata",
    )
    return {
        "join_url": meeting.get("join_url", ""),
        "meeting_id": str(meeting.get("id", "")),
        "slot_start_ist": slot_start_ist,
        "slot_end_ist": slot_end_ist,
        "source": "zoom_provider",
    }


def verified_send_for_candidate(
    candidate: dict[str, Any], slot_start_ist: str, slot_end_ist: str, job_spec: dict[str, Any]
) -> dict[str, Any]:
    decision = candidate.get("final_decision", "rejected")
    to_email = candidate.get("email", "")
    name = candidate.get("name", "Candidate")
    title = job_spec.get("title", "the role")
    job_id = job_spec.get("job_id", "JOB-001")
    match = int(candidate.get("match_percent", 0) or 0)
    shortlist_min, reject_max = thresholds(job_spec)

    if decision == "selected":
        meeting = zoom_create_with_provider(name, slot_start_ist, slot_end_ist)
        subject = f"Interview Invitation - {title}"
        date_label = interview_date_label()
        body = (
            f"Hello {name},\n\n"
            f"We are pleased to inform you that you have been selected to proceed to the next stage "
            f"of our recruitment process for the {title} position, Job ID: {job_id}. "
            "We were impressed by your background and experience, and we would like to invite you "
            "to an interview to further discuss your qualifications.\n\n"
            "The interview details are as follows:\n"
            f"Date and Time: {date_label} at {slot_start_ist}\n"
            "Timezone: Asia/Kolkata, IST, UTC+05:30\n"
            f"Zoom Link: {meeting.get('join_url', '')}\n\n"
            "Please join the meeting using the provided Zoom link at the scheduled time. "
            "We look forward to speaking with you and exploring how your skills and experience align "
            "with our team's needs.\n\n"
            "If you have any questions or concerns, please do not hesitate to reach out to us.\n\n"
            "Best regards,\nHR Team"
        )
        send_status = send_email_dynamic(to_email=to_email, subject=subject, body=body)
        return {
            "candidate_id": candidate.get("candidate_id", ""),
            "candidate_name": name,
            "email": to_email,
            "final_decision": decision,
            "meeting": meeting,
            "meeting_source": meeting.get("source", "unknown"),
            "send_status": send_status,
        }

    subject = f"Application Update - {title}"
    if reject_max < match < shortlist_min:
        reason_line = (
            "Although your skills and experience are impressive, your assessment score fell between "
            "our thresholds, making it a competitive decision."
        )
    else:
        reason_line = (
            "Although your profile is valuable, we are proceeding with candidates who more closely "
            "match our current shortlist criteria."
        )
    body = (
        f"Dear {name},\n\n"
        f"We appreciate the time you took to apply for the {title} position, {job_id}, at our company. "
        "After careful consideration, we regret to inform you that we will not be moving forward with "
        "your application at this time.\n\n"
        f"{reason_line} "
        "Please know that this decision is not a reflection on your abilities, but rather a result of the "
        "high caliber of candidates we received for this role.\n\n"
        "We appreciate your interest in joining our team and wish you the best of luck in your job search. "
        "If you have any questions or would like feedback on your application, please do not hesitate to reach out.\n\n"
        "Best regards,\nHR Team"
    )
    send_status = send_email_dynamic(to_email=to_email, subject=subject, body=body)
    return {
        "candidate_id": candidate.get("candidate_id", ""),
        "candidate_name": name,
        "email": to_email,
        "final_decision": decision,
        "send_status": send_status,
    }
