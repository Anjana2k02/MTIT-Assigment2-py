from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator
from app.models.billing import OrderType, PosStatus


class BillItemDetail(BaseModel):
    item_id: str
    name: str
    price: float
    quantity: int
    subtotal: float


class BillResponse(BaseModel):
    order_id: str
    order_type: OrderType
    customer_name: Optional[str] = None
    table_number: Optional[int] = None
    delivery_address: Optional[str] = None
    items: List[BillItemDetail]
    subtotal: float
    discount_name: str
    discount_percent: float
    discount_amount: float
    after_discount: float
    tax: float
    total: float
    status: PosStatus
    created_at: datetime

    @field_validator("order_id", mode="before")
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None
