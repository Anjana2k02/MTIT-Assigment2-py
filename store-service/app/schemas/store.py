from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class StoreBase(BaseModel):
    store_name: str
    description: Optional[str] = None


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    store_name: Optional[str] = None
    description: Optional[str] = None


class StoreResponse(StoreBase):
    id: Optional[str] = None
    created_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None

    class Config:
        from_attributes = True