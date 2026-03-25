from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator
from app.models.billing import OrderType, PosStatus


class PosItemRequest(BaseModel):
    item_id: str
    quantity: int


class PosItemResponse(BaseModel):
    item_id: str
    name: str
    price: float
    quantity: int
    subtotal: float


class PosCreate(BaseModel):
    order_type: OrderType
    customer_name: Optional[str] = None
    table_number: Optional[int] = None       # for dining
    delivery_address: Optional[str] = None   # for delivery
    items: List[PosItemRequest]
    discount_id: Optional[str] = None        # Discount document ID (None = no discount)
    tax_rate: float = 0.0                    # e.g. 0.10 for 10%


class PosUpdate(BaseModel):
    customer_name: Optional[str] = None
    table_number: Optional[int] = None
    delivery_address: Optional[str] = None
    discount_id: Optional[str] = None
    status: Optional[PosStatus] = None
    tax_rate: Optional[float] = None


class PosResponse(BaseModel):
    id: Optional[str] = None
    order_type: OrderType
    customer_name: Optional[str] = None
    table_number: Optional[int] = None
    delivery_address: Optional[str] = None
    items: List[PosItemResponse]
    discount_id: Optional[str] = None
    subtotal: float
    tax: float
    total: float
    status: PosStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_id(cls, v):
        return str(v) if v is not None else None

    class Config:
        from_attributes = True
