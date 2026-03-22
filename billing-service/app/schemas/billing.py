from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.billing import InvoiceStatus


class InvoiceBase(BaseModel):
    order_id: int
    customer_name: str
    subtotal: float
    tax: float = 0.0
    total: float


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    customer_name: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    status: Optional[InvoiceStatus] = None


class InvoiceResponse(InvoiceBase):
    id: int
    status: InvoiceStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
