# How to Get Zoom API Key for Meetings (Modern Method)

Zoom no longer recommends old JWT API keys.

Use:

## ✅ Server-to-Server OAuth App

This gives:

* `Account ID`
* `Client ID`
* `Client Secret`

Used for:

* Create meetings
* Manage meetings
* Get recordings
* Webinar APIs
* User APIs

JWT apps are deprecated by Zoom.

---

# Step-by-Step

## 1. Open Zoom Developer Marketplace

[Zoom App Marketplace](https://marketplace.zoom.us/)

Login with your Zoom account.

---

# 2. Create App

Go to:

[Create Zoom App Page](https://marketplace.zoom.us/develop/create)

---

# 3. Select

Choose:

```text
Server-to-Server OAuth
```

Click:

```text
Create
```


---

# 4. Enter App Name

Example:

```text
MeetingAutomationApp
```

Click:

```text
Create
```

---

# 5. Copy Credentials

You will get:

```text
Account ID
Client ID
Client Secret
```

These are your Zoom API credentials.

---

# 6. Configure Information

Fill:

* company name
* developer email
* contact name

Otherwise app activation fails.
---

# 7. Add Scopes

Go:

```text
Scopes → Add Scopes
```

For meetings add:

```text
meeting:read:list_meetings:admin
meeting:write:invite_links:admin
meeting:write:meeting:admin
meeting:read:meeting:admin
user:read:user:admin
```
---

# 8. Activate App

Click:

```text
Activate your app
```

---

# 9. Generate Access Token

Use:

```bash
curl -X POST \
https://zoom.us/oauth/token?grant_type=account_credentials&account_id=YOUR_ACCOUNT_ID \
-u CLIENT_ID:CLIENT_SECRET
```

Returns:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600
}
```


---

# 10. Create Meeting Example

## Python

```python
import requests

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "topic": "AI Meeting",
    "type": 2,
    "start_time": "2026-05-17T10:00:00",
    "duration": 30,
    "timezone": "Asia/Kolkata"
}

response = requests.post(
    "https://api.zoom.us/v2/users/me/meetings",
    headers=headers,
    json=payload
)

print(response.json())
```

---

# Important Notes

| Item              | Details             |
| ----------------- | ------------------- |
| JWT App           | ❌ Deprecated        |
| OAuth App         | ✅ Recommended       |
| Free Zoom Account | Limited APIs        |
| Paid Account      | Better meeting APIs |
| Token Expiry      | 1 hour              |

Regex --> id="[^"]*"

---

# Official Docs

* [Zoom S2S OAuth Docs](https://developers.zoom.us/docs/internal-apps/s2s-oauth/)
* [Create S2S OAuth App](https://developers.zoom.us/docs/internal-apps/create/)
* [Zoom API Reference](https://developers.zoom.us/docs/api/)

[1]: https://docs.themeum.com/tutor-lms/tutorials/how-to-migrate-from-zoom-jwt-to-server-to-server-oauth/ "How to Migrate From Zoom JWT App to Server-To- ..."
[2]: https://developers.zoom.us/docs/internal-apps/create/ "Create a Server-to-Server OAuth app - Internal Apps"
[3]: https://help.vidizmo.ai/docs/Integration%20and%20Customization/Zoom/How%20to%20create%20ZOOM%20Server-to-Server%20OAuth%20App%20in%20ZOOM%20Marketplace/ "How to create ZOOM Server-to-Server OAuth App in ZOOM ..."
[4]: https://jenzushsu.medium.com/setting-up-server-to-server-s2s-oauth-to-test-zoom-apis-via-postman-32c9cd7a73 "Setting up Server-to-Server (S2S) OAuth to test Zoom APIs via ..."
[5]: https://composio.dev/auth/zoom "How to create OAuth2 credentials for Zoom and configure it ..."
[6]: https://developers.zoom.us/docs/internal-apps/s2s-oauth/ "Server-to-Server OAuth - Internal Apps"
[7]: https://community.zoom.com/marketplace-10/server-to-server-oauth-app-returns-error-124-invalid-access-token-despite-valid-credentials-79791 "Server-to-Server OAuth App Returns Error 124 Invalid ..."

# Get Brevo API key
https://app.brevo.com/settings/keys/api