from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=List[OrderResponse])
async def get_orders():
    return await order_service.get_all()


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    order = await order_service.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate):
    return await order_service.create(order)


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: str, order: OrderUpdate):
    updated = await order_service.update(order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated


@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: str):
    deleted = await order_service.delete(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
