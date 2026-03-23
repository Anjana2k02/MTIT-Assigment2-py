from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class DiscountCreate(BaseModel):
    name: str
    amount: float                # percentage, e.g. 10.0 = 10%


class DiscountUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None


class DiscountResponse(BaseModel):
    id: Optional[str] = None
    name: str
    amount: float
    created_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None

    class Config:
        from_attributes = True
