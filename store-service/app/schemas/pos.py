from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class POSBase(BaseModel):
    store_id: str
    pos_name: str
    description: Optional[str] = None


class POSCreate(POSBase):
    pass


class POSUpdate(BaseModel):
    store_id: Optional[str] = None
    pos_name: Optional[str] = None
    description: Optional[str] = None


class POSResponse(POSBase):
    id: Optional[str] = None
    created_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None

    class Config:
        from_attributes = True