from pydantic import BaseModel
from typing import Optional
from app.models.table import TableStatus


class TableBase(BaseModel):
    table_number: int
    capacity: int
    status: TableStatus = TableStatus.AVAILABLE


class TableCreate(TableBase):
    pass


class TableUpdate(BaseModel):
    table_number: Optional[int] = None
    capacity: Optional[int] = None
    status: Optional[TableStatus] = None


class TableResponse(TableBase):
    id: Optional[str] = None

    class Config:
        from_attributes = True
