from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field


class Location(Document):
    location_name: str
    description: Optional[str] = None
    availability: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "locations"
