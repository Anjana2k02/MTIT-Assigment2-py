import enum
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field


class DeliveryStatus(str, enum.Enum):
    PENDING = "pending"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"


class Delivery(Document):
    order_id: int
    customer_address: str
    driver_name: Optional[str] = None
    status: DeliveryStatus = DeliveryStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "deliveries"
