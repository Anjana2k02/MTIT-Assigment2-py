from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.store import StoreCreate, StoreUpdate, StoreResponse
from app.services import store_service

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("/", response_model=List[StoreResponse])
async def get_stores():
    return await store_service.get_all()


@router.get("/{store_id}", response_model=StoreResponse)
async def get_store(store_id: str):
    store = await store_service.get_by_id(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.post("/", response_model=StoreResponse, status_code=201)
async def create_store(store: StoreCreate):
    return await store_service.create(store)


@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(store_id: str, store: StoreUpdate):
    updated = await store_service.update(store_id, store)
    if not updated:
        raise HTTPException(status_code=404, detail="Store not found")
    return updated


@router.delete("/{store_id}")
async def delete_store(store_id: str):
    deleted = await store_service.delete(store_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Store not found")
    return {"message": "Store deleted successfully"}