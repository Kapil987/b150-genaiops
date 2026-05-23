import os
from typing import Any, Dict

import requests


def send_email_dynamic(to_email: str, subject: str, body: str) -> Dict[str, Any]:
    brevo_api_key = os.getenv("BREVO_API_KEY")
    if not brevo_api_key:
        return {
            "sent": False,
            "dry_run": True,
            "to": to_email,
            "provider": "mygoogle",
            "reason": "BREVO_API_KEY is not configured.",
        }

    sender_email = os.getenv("BREVO_SENDER_EMAIL", "shobhansingh431@gmail.com")
    sender_name = os.getenv("BREVO_SENDER_NAME", "HR Team")
    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": body.replace("\n", "<br>"),
        "textContent": body,
    }
    headers = {
        "api-key": brevo_api_key,
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            json=payload,
            headers=headers,
            timeout=30,
        )
        if 200 <= resp.status_code < 300:
            return {"sent": True, "dry_run": False, "to": to_email, "provider": "brevo"}
        reason = f"Brevo error {resp.status_code}: {resp.text[:300]}"
        return {"sent": False, "dry_run": False, "to": to_email, "provider": "brevo", "reason": reason}
    except Exception as exc:
        return {"sent": False, "dry_run": False, "to": to_email, "provider": "brevo", "reason": str(exc)}
