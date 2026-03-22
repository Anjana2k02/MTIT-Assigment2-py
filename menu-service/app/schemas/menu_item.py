from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from app.schemas.item import ItemResponse


class MenuItemBase(BaseModel):
    item_id: str
    menu_id: str
    availability: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    availability: Optional[bool] = None


class MenuItemResponse(MenuItemBase):
    id: Optional[str] = None
    created_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None

    class Config:
        from_attributes = True


class MenuItemDetailResponse(BaseModel):
    """Used by GET /menus/{menu_id}/items — enriched with full item data."""
    id: Optional[str] = None
    menu_id: str
    availability: bool
    created_at: datetime
    item: Optional[ItemResponse] = None

    class Config:
        from_attributes = True
