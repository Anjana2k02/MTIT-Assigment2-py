from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.delivery import DeliveryStatus


class DeliveryBase(BaseModel):
    order_id: int
    customer_address: str
    driver_name: Optional[str] = None


class DeliveryCreate(DeliveryBase):
    pass


class DeliveryUpdate(BaseModel):
    customer_address: Optional[str] = None
    driver_name: Optional[str] = None
    status: Optional[DeliveryStatus] = None


class DeliveryResponse(DeliveryBase):
    id: Optional[str] = None
    status: DeliveryStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
