from app.core.security import create_access_token, verify_password
from app.core.users import get_user


class AuthService:
    def authenticate(self, username: str, password: str) -> str:
        user = get_user(username)

        print("USERNAME:", username)
        print("PASSWORD:", password)
        print("USER FOUND:", bool(user))

        if not user or not verify_password(password, user["hashed_password"]):
            raise ValueError("Invalid credentials")

        return create_access_token(subject=username)
