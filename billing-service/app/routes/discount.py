from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.discount import DiscountCreate, DiscountUpdate, DiscountResponse
from app.services import discount_service

router = APIRouter(prefix="/discounts", tags=["discount"])


@router.get("/", response_model=List[DiscountResponse])
async def get_discounts():
    return await discount_service.get_all()


@router.get("/{discount_id}", response_model=DiscountResponse)
async def get_discount(discount_id: str):
    discount = await discount_service.get_by_id(discount_id)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount


@router.post("/", response_model=DiscountResponse, status_code=201)
async def create_discount(discount: DiscountCreate):
    return await discount_service.create(discount)


@router.put("/{discount_id}", response_model=DiscountResponse)
async def update_discount(discount_id: str, discount: DiscountUpdate):
    updated = await discount_service.update(discount_id, discount)
    if not updated:
        raise HTTPException(status_code=404, detail="Discount not found")
    return updated


@router.delete("/{discount_id}", status_code=204)
async def delete_discount(discount_id: str):
    deleted = await discount_service.delete(discount_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Discount not found")
