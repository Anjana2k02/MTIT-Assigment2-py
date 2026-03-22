import enum
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field


class ItemType(str, enum.Enum):
    KOT = "KOT"
    BOT = "BOT"
    Other = "Other"


class Item(Document):
    item_name: str
    item_price: float
    item_type: ItemType
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "items"
