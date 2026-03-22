from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate


async def get_all(db: AsyncSession) -> List[Order]:
    result = await db.execute(select(Order))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, order_id: int) -> Optional[Order]:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: OrderCreate) -> Order:
    order = Order(**data.model_dump())
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def update(db: AsyncSession, order_id: int, data: OrderUpdate) -> Optional[Order]:
    order = await get_by_id(db, order_id)
    if not order:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    await db.commit()
    await db.refresh(order)
    return order


async def delete(db: AsyncSession, order_id: int) -> bool:
    order = await get_by_id(db, order_id)
    if not order:
        return False
    await db.delete(order)
    await db.commit()
    return True
