import enum
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Document):
    customer_name: str
    table_id: Optional[int] = None
    status: OrderStatus = OrderStatus.PENDING
    total_amount: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "orders"
