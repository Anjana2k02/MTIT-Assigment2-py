import enum
from datetime import datetime
from typing import List, Optional
from beanie import Document
from pydantic import BaseModel, Field


class OrderType(str, enum.Enum):
    DINING = "dining"
    DELIVERY = "delivery"


class PosStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class PosItem(BaseModel):
    item_id: str
    name: str
    price: float
    quantity: int
    subtotal: float


class PosOrder(Document):
    order_type: OrderType
    customer_name: Optional[str] = None
    table_number: Optional[int] = None       # for dining orders
    delivery_address: Optional[str] = None   # for delivery orders
    items: List[PosItem] = []
    discount_id: Optional[str] = None        # reference to Discount document
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    status: PosStatus = PosStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "pos_orders"
