from app.core.security import hash_password

hashed_password = hash_password("admin")

_fake_users_db = {
    "admin@example.com": {
        "username": "admin@example.com",
        "hashed_password": hashed_password,
    }
}


def get_user(username: str) -> dict | None:
    return _fake_users_db.get(username)
