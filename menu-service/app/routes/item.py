from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services import item_service

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=List[ItemResponse])
async def get_items():
    return await item_service.get_all()


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    item = await item_service.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    return await item_service.create(item)


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemUpdate):
    updated = await item_service.update(item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: str):
    deleted = await item_service.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
