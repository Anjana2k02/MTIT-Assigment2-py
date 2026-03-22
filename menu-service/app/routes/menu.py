from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.menu import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.services import menu_service

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/", response_model=List[MenuItemResponse])
async def get_menu_items():
    return await menu_service.get_all()


@router.get("/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(item_id: str):
    item = await menu_service.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@router.post("/", response_model=MenuItemResponse, status_code=201)
async def create_menu_item(item: MenuItemCreate):
    return await menu_service.create(item)


@router.put("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(item_id: str, item: MenuItemUpdate):
    updated = await menu_service.update(item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated


@router.delete("/{item_id}", status_code=204)
async def delete_menu_item(item_id: str):
    deleted = await menu_service.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menu item not found")
