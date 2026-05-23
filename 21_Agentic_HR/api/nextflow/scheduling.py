from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


INTERVIEW_SCHEDULE_OFFSET_DAYS = 1
IST_ZONE = ZoneInfo("Asia/Kolkata")


def interview_date_ist() -> date:
    return datetime.now(IST_ZONE).date() + timedelta(days=INTERVIEW_SCHEDULE_OFFSET_DAYS)


def interview_datetime_ist(slot_time_ist: str) -> datetime:
    return datetime.strptime(f"{interview_date_ist()} {slot_time_ist}", "%Y-%m-%d %H:%M").replace(
        tzinfo=IST_ZONE
    )


def interview_date_label() -> str:
    return interview_date_ist().strftime("%A, %d %B %Y")
