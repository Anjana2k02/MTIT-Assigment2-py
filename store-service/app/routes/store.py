from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.store import StoreItemCreate, StoreItemUpdate, StoreItemResponse
from app.services import store_service

router = APIRouter(prefix="/store", tags=["store"])


@router.get("/", response_model=List[StoreItemResponse])
async def get_store_items():
    return await store_service.get_all()


@router.get("/{item_id}", response_model=StoreItemResponse)
async def get_store_item(item_id: str):
    item = await store_service.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Store item not found")
    return item


@router.post("/", response_model=StoreItemResponse, status_code=201)
async def create_store_item(item: StoreItemCreate):
    return await store_service.create(item)


@router.put("/{item_id}", response_model=StoreItemResponse)
async def update_store_item(item_id: str, item: StoreItemUpdate):
    updated = await store_service.update(item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Store item not found")
    return updated


@router.delete("/{item_id}", status_code=204)
async def delete_store_item(item_id: str):
    deleted = await store_service.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Store item not found")
