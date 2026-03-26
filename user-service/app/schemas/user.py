from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr
    address: Optional[str] = None
    phoneNo: Optional[str] = None
    role_id: Optional[str] = None


class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSignIn(BaseModel):
    username: str
    password: str


class UserSignInOut(BaseModel):
    username: str
    role: str = "user"

class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phoneNo: Optional[str] = None
    role_id: Optional[str] = None
    password: Optional[str] = None


class UserOut(UserBase):
    user_id: str
