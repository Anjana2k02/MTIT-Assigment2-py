from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate, DeliveryResponse
from app.services import delivery_service

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("/", response_model=List[DeliveryResponse])
async def get_deliveries(db: AsyncSession = Depends(get_db)):
    return await delivery_service.get_all(db)


@router.get("/{delivery_id}", response_model=DeliveryResponse)
async def get_delivery(delivery_id: int, db: AsyncSession = Depends(get_db)):
    delivery = await delivery_service.get_by_id(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery


@router.post("/", response_model=DeliveryResponse, status_code=201)
async def create_delivery(delivery: DeliveryCreate, db: AsyncSession = Depends(get_db)):
    return await delivery_service.create(db, delivery)


@router.put("/{delivery_id}", response_model=DeliveryResponse)
async def update_delivery(delivery_id: int, delivery: DeliveryUpdate, db: AsyncSession = Depends(get_db)):
    updated = await delivery_service.update(db, delivery_id, delivery)
    if not updated:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return updated


@router.delete("/{delivery_id}", status_code=204)
async def delete_delivery(delivery_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delivery_service.delete(db, delivery_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery not found")
