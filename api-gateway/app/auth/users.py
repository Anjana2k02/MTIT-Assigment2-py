import hmac

# Demo users for assignment use. Replace with persistent storage in production.
_USERS = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "staff": {"username": "staff", "password": "staff123", "role": "staff"},
}


def authenticate_user(username: str, password: str):
    user = _USERS.get(username)
    if not user:
        return None

    if not hmac.compare_digest(user["password"], password):
        return None

    return {"username": user["username"], "role": user["role"]}
