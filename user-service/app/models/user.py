from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: str
    username: str
    email: str
    password_hash: Optional[str] = None
    address: Optional[str] = None
    phoneNo: Optional[str] = None
    role_id: Optional[str] = None
