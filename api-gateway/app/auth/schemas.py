from pydantic import BaseModel, Field


class SignInRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=3, max_length=128)


class SignUpRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=3, max_length=128)


class LoginRequest(SignInRequest):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
