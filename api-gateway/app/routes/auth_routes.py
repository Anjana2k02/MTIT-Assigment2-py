from fastapi import APIRouter, HTTPException, status

from app.auth.jwt import create_access_token
from app.auth.schemas import LoginRequest, SignInRequest, SignUpRequest, TokenResponse
from app.auth.users import authenticate_user, signup_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    return await signin(SignInRequest(**payload.dict()))


@router.post("/signin", response_model=TokenResponse)
async def signin(payload: SignInRequest):
    try:
        user = await authenticate_user(payload.username, payload.password)
    except RuntimeError as ex:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(ex),
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token(subject=user["username"], role=user["role"])
    return TokenResponse(
        access_token=token,
        expires_in=settings.JWT_EXPIRE_MINUTES * 60,
    )


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(payload: SignUpRequest):
    try:
        return await signup_user(payload.username, payload.email, payload.password)
    except RuntimeError as ex:
        message = str(ex).lower()
        http_status = status.HTTP_400_BAD_REQUEST
        if "already" in message or "exist" in message:
            http_status = status.HTTP_409_CONFLICT
        raise HTTPException(status_code=http_status, detail=str(ex))
