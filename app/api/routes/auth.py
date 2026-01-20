from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    service = AuthService()

    try:
        token = service.authenticate(payload.username, payload.password)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials") from None

    return TokenResponse(access_token=token)
