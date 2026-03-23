from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class LocationBase(BaseModel):
    location_name: str
    description: Optional[str] = None
    availability: bool = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    location_name: Optional[str] = None
    description: Optional[str] = None
    availability: Optional[bool] = None


class LocationResponse(LocationBase):
    id: Optional[str] = None
    created_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None

    class Config:
        from_attributes = True
