from beanie import Document
from typing import Optional


class MenuItem(Document):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    available: bool = True

    class Settings:
        name = "menu_items"
