from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field


class POS(Document):
    store_id: str
    pos_name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "pos"