from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.delivery import DeliveryStatus


class DeliveryBase(BaseModel):
    order_id: int
    customer_name: str
    customer_address: str
    customer_phone_number: str
    driver_name: Optional[str] = None
    status: DeliveryStatus = DeliveryStatus.PENDING


class DeliveryCreate(DeliveryBase):
    pass


class DeliveryUpdate(BaseModel):
    order_id: Optional[int] = None
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    customer_phone_number: Optional[str] = None
    driver_name: Optional[str] = None
    status: Optional[DeliveryStatus] = None


class DeliveryResponse(DeliveryBase):
    id: Optional[str] = None
    order_id: int
    customer_name: str
    customer_address: str
    customer_phone_number: str
    driver_name: Optional[str] = None
    status: DeliveryStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
