from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.menu import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.services import menu_service

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/", response_model=List[MenuItemResponse])
async def get_menu_items(db: AsyncSession = Depends(get_db)):
    return await menu_service.get_all(db)


@router.get("/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await menu_service.get_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@router.post("/", response_model=MenuItemResponse, status_code=201)
async def create_menu_item(item: MenuItemCreate, db: AsyncSession = Depends(get_db)):
    return await menu_service.create(db, item)


@router.put("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(item_id: int, item: MenuItemUpdate, db: AsyncSession = Depends(get_db)):
    updated = await menu_service.update(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated


@router.delete("/{item_id}", status_code=204)
async def delete_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await menu_service.delete(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menu item not found")
