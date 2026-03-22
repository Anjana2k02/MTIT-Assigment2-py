from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.menu import MenuItem
from app.schemas.menu import MenuItemCreate, MenuItemUpdate


async def get_all(db: AsyncSession) -> List[MenuItem]:
    result = await db.execute(select(MenuItem))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, item_id: int) -> Optional[MenuItem]:
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: MenuItemCreate) -> MenuItem:
    item = MenuItem(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def update(db: AsyncSession, item_id: int, data: MenuItemUpdate) -> Optional[MenuItem]:
    item = await get_by_id(db, item_id)
    if not item:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item


async def delete(db: AsyncSession, item_id: int) -> bool:
    item = await get_by_id(db, item_id)
    if not item:
        return False
    await db.delete(item)
    await db.commit()
    return True
