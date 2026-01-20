from app.core.security import create_access_token, verify_password
from app.core.users import get_user


class AuthService:
    def authenticate(self, username: str, password: str) -> str:
        user = get_user(username)
        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user["hashed_password"]):
            raise ValueError("Invalid credentials")

        return create_access_token(subject=username)
