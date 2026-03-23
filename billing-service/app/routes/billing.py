import httpx
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.billing import PosCreate, PosUpdate, PosResponse
from app.services import billing_service

router = APIRouter(prefix="/pos", tags=["pos"])


@router.get("/", response_model=List[PosResponse])
async def get_pos_orders():
    return await billing_service.get_all()


@router.get("/delivery", response_model=List[PosResponse])
async def get_delivery_orders():
    """Return all delivery-type POS orders."""
    return await billing_service.get_delivery_orders()


@router.get("/{order_id}", response_model=PosResponse)
async def get_pos_order(order_id: str):
    order = await billing_service.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="POS order not found")
    return order


@router.post("/", response_model=PosResponse, status_code=201)
async def create_pos_order(order: PosCreate):
    try:
        return await billing_service.create(order)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Menu item lookup failed: {e.response.status_code} — {e.response.text}",
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Menu Service unreachable: {e}",
        )


@router.put("/{order_id}", response_model=PosResponse)
async def update_pos_order(order_id: str, order: PosUpdate):
    updated = await billing_service.update(order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="POS order not found")
    return updated


@router.delete("/{order_id}", status_code=204)
async def delete_pos_order(order_id: str):
    deleted = await billing_service.delete(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="POS order not found")
