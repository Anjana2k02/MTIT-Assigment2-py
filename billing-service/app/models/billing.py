import enum
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field


class InvoiceStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class Invoice(Document):
    order_id: int
    customer_name: str
    subtotal: float
    tax: float = 0.0
    total: float
    status: InvoiceStatus = InvoiceStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "invoices"
