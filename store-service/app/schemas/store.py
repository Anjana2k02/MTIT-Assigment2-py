from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StoreItemBase(BaseModel):
    name: str
    quantity: float
    unit: str
    min_quantity: float = 0.0


class StoreItemCreate(StoreItemBase):
    pass


class StoreItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    min_quantity: Optional[float] = None


class StoreItemResponse(StoreItemBase):
    id: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
