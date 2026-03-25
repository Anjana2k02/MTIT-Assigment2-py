from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.pos import POSCreate, POSUpdate, POSResponse
from app.services import pos_service

router = APIRouter(prefix="/pos", tags=["pos"])


@router.get("/", response_model=List[POSResponse])
async def get_pos_list():
    return await pos_service.get_all()


@router.get("/store/{store_id}", response_model=List[POSResponse])
async def get_pos_by_store(store_id: str):
    return await pos_service.get_by_store_id(store_id)


@router.get("/{pos_id}", response_model=POSResponse)
async def get_pos(pos_id: str):
    pos = await pos_service.get_by_id(pos_id)
    if not pos:
        raise HTTPException(status_code=404, detail="POS not found")
    return pos


@router.post("/", response_model=POSResponse, status_code=201)
async def create_pos(pos: POSCreate):
    created = await pos_service.create(pos)
    if not created:
        raise HTTPException(status_code=404, detail="Store not found")
    return created


@router.put("/{pos_id}", response_model=POSResponse)
async def update_pos(pos_id: str, pos: POSUpdate):
    updated = await pos_service.update(pos_id, pos)
    if not updated:
        raise HTTPException(status_code=404, detail="POS not found")
    return updated


@router.delete("/{pos_id}")
async def delete_pos(pos_id: str):
    deleted = await pos_service.delete(pos_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="POS not found")
    return {"message": "POS deleted successfully"}