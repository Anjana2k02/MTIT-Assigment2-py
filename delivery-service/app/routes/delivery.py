from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate, DeliveryResponse
from app.services import delivery_service

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("/", response_model=List[DeliveryResponse])
async def get_deliveries():
    return await delivery_service.get_all()


@router.get("/{delivery_id}", response_model=DeliveryResponse)
async def get_delivery(delivery_id: str):
    delivery = await delivery_service.get_by_id(delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery


@router.post("/", response_model=DeliveryResponse, status_code=201)
async def create_delivery(delivery: DeliveryCreate):
    return await delivery_service.create(delivery)


@router.put("/{delivery_id}", response_model=DeliveryResponse)
async def update_delivery(delivery_id: str, delivery: DeliveryUpdate):
    updated = await delivery_service.update(delivery_id, delivery)
    if not updated:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return updated


@router.delete("/{delivery_id}", status_code=204)
async def delete_delivery(delivery_id: str):
    deleted = await delivery_service.delete(delivery_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery not found")
