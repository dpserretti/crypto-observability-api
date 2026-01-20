ADMIN_HASHED_PASSWORD = "$2b$12$XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

_fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": ADMIN_HASHED_PASSWORD,
    }
}


def get_user(username: str) -> dict | None:
    return _fake_users_db.get(username)
