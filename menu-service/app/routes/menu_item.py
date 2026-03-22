from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse, MenuItemDetailResponse
from app.services import menu_item_service

router = APIRouter(prefix="/menu-items", tags=["menu-items"])

# Separate router for the nested /menus/{menu_id}/items endpoint
menus_router = APIRouter(prefix="/menus", tags=["menus"])


@router.get("/", response_model=List[MenuItemResponse])
async def get_menu_items():
    return await menu_item_service.get_all()


@router.get("/{menu_item_id}", response_model=MenuItemResponse)
async def get_menu_item(menu_item_id: str):
    mi = await menu_item_service.get_by_id(menu_item_id)
    if not mi:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return mi


@router.post("/", response_model=MenuItemResponse, status_code=201)
async def create_menu_item(data: MenuItemCreate):
    return await menu_item_service.create(data)


@router.put("/{menu_item_id}", response_model=MenuItemResponse)
async def update_menu_item(menu_item_id: str, data: MenuItemUpdate):
    updated = await menu_item_service.update(menu_item_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated


@router.delete("/{menu_item_id}", status_code=204)
async def delete_menu_item(menu_item_id: str):
    deleted = await menu_item_service.delete(menu_item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menu item not found")


@menus_router.get("/{menu_id}/items", response_model=List[MenuItemDetailResponse])
async def get_items_in_menu(menu_id: str):
    return await menu_item_service.get_items_in_menu(menu_id)
