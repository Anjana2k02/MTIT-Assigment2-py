from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from app.models.item import ItemType


class ItemBase(BaseModel):
    item_name: str
    item_price: float
    item_type: ItemType
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    item_name: Optional[str] = None
    item_price: Optional[float] = None
    item_type: Optional[ItemType] = None
    description: Optional[str] = None


class ItemResponse(ItemBase):
    id: Optional[str] = None
    created_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None

    class Config:
        from_attributes = True
