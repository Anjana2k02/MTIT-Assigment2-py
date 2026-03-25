import httpx

from app.config import settings


async def authenticate_user(username: str, password: str):
    payload = {"username": username, "password": password}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{settings.USER_SERVICE_URL}/users/signin", json=payload)
    except httpx.HTTPError:
        raise RuntimeError("Unable to reach user service")

    if resp.status_code == 401:
        return None

    if resp.status_code >= 400:
        detail = _extract_detail(resp)
        raise RuntimeError(detail)

    data = resp.json()
    return {
        "username": data.get("username", username),
        "role": data.get("role", "user"),
    }


async def signup_user(username: str, email: str, password: str):
    payload = {"username": username, "email": email, "password": password}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{settings.USER_SERVICE_URL}/users/signup", json=payload)
    except httpx.HTTPError:
        raise RuntimeError("Unable to reach user service")

    if resp.status_code >= 400:
        raise RuntimeError(_extract_detail(resp))

    return resp.json()


def _extract_detail(resp: httpx.Response) -> str:
    try:
        payload = resp.json()
        if isinstance(payload, dict) and "detail" in payload:
            return str(payload["detail"])
    except Exception:
        pass
    return f"User service request failed with status {resp.status_code}"
