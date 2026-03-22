from datetime import datetime
from beanie import Document
from pydantic import Field


class StoreItem(Document):
    name: str
    quantity: float = 0.0
    unit: str
    min_quantity: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "store_items"
