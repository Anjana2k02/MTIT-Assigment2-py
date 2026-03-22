from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.order import OrderStatus


class OrderBase(BaseModel):
    customer_name: str
    table_id: Optional[int] = None
    total_amount: float = 0.0


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    table_id: Optional[int] = None
    status: Optional[OrderStatus] = None
    total_amount: Optional[float] = None


class OrderResponse(OrderBase):
    id: Optional[str] = None
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
