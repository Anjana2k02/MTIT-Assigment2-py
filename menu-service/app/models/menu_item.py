from datetime import datetime
from beanie import Document
from pydantic import Field


class MenuItem(Document):
    item_id: str
    menu_id: str
    availability: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "menu_items"
