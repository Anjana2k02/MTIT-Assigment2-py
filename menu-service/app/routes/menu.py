from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.menu import MenuCreate, MenuUpdate, MenuResponse
from app.services import menu_service

router = APIRouter(prefix="/menus", tags=["menus"])


@router.get("/", response_model=List[MenuResponse])
async def get_menus():
    return await menu_service.get_all()


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu(menu_id: str):
    menu = await menu_service.get_by_id(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu


@router.post("/", response_model=MenuResponse, status_code=201)
async def create_menu(menu: MenuCreate):
    return await menu_service.create(menu)


@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu(menu_id: str, menu: MenuUpdate):
    updated = await menu_service.update(menu_id, menu)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu not found")
    return updated


@router.delete("/{menu_id}", status_code=204)
async def delete_menu(menu_id: str):
    deleted = await menu_service.delete(menu_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menu not found")
