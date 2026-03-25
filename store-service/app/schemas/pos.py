from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class POSBase(BaseModel):
    store_id: str
    POS_name: str
    description: Optional[str] = None


class POSCreate(POSBase):
    pass


class POSUpdate(BaseModel):
    store_id: Optional[str] = None
    POS_name: Optional[str] = None
    description: Optional[str] = None


class POSResponse(POSBase):
    id: Optional[str] = None
    create_At: datetime

    @field_validator('id', mode='before')
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None

    class Config:
        from_attributes = True