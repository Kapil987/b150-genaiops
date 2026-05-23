import base64
import os
from typing import Any, Dict, Optional

import requests


def get_zoom_token_dynamic() -> Optional[str]:
    account_id = os.getenv("ACCOUNT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not all([account_id, client_id, client_secret]):
        return None

    token_url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={account_id}"
    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {"Authorization": f"Basic {b64_auth}"}

    response = requests.post(token_url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json().get("access_token")


def create_zoom_meeting_dynamic(
    token: str,
    topic: str,
    start_time_iso: str,
    duration_minutes: int,
    timezone_name: str,
) -> Dict[str, Any]:
    url = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "topic": topic,
        "type": 2,
        "start_time": start_time_iso,
        "duration": duration_minutes,
        "timezone": timezone_name,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
