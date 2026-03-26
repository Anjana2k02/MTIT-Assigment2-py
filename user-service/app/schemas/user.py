from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    address: Optional[str] = None
    phoneNo: Optional[str] = None
    role_id: int

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    user_id: int
    model_config = ConfigDict(from_attributes=True)
