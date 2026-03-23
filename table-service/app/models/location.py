from beanie import Document
from pydantic import Field
from datetime import datetime

class Location(Document):
    location_name: str
    description: str
    availability: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "locations"