from typing import Optional
from pydantic import BaseModel, field_validator
from app.schemas.table_status import TableStatusResponse


class TableBase(BaseModel):
    location_id: str
    table_name: str
    status: int   # status_id (0, 1, 2) from TableStatus collection


class TableCreate(TableBase):
    pass


class TableUpdate(BaseModel):
    location_id: Optional[str] = None
    table_name: Optional[str] = None
    status: Optional[int] = None


class TableResponse(TableBase):
    id: Optional[str] = None

    @field_validator('id', mode='before')
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None

    class Config:
        from_attributes = True


class TableDetailResponse(BaseModel):
    """Used by GET /locations/{location_id}/tables — enriched with status details."""
    id: Optional[str] = None
    location_id: str
    table_name: str
    status: int
    status_detail: Optional[TableStatusResponse] = None

    class Config:
        from_attributes = True
