from typing import Optional
from pydantic import BaseModel, field_validator


class TableStatusBase(BaseModel):
    status_id: int
    type: str


class TableStatusCreate(TableStatusBase):
    pass


class TableStatusUpdate(BaseModel):
    status_id: Optional[int] = None
    type: Optional[str] = None


class TableStatusResponse(TableStatusBase):
    id: Optional[str] = None

    @field_validator('id', mode='before')
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None

    class Config:
        from_attributes = True
