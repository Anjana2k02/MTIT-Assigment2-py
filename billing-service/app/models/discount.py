from datetime import datetime
from beanie import Document
from pydantic import Field


class Discount(Document):
    name: str
    amount: float                                    # percentage, e.g. 10.0 = 10%
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "discounts"
