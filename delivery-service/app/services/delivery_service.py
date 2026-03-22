from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.delivery import Delivery
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate


async def get_all(db: AsyncSession) -> List[Delivery]:
    result = await db.execute(select(Delivery))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, delivery_id: int) -> Optional[Delivery]:
    result = await db.execute(select(Delivery).where(Delivery.id == delivery_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: DeliveryCreate) -> Delivery:
    delivery = Delivery(**data.model_dump())
    db.add(delivery)
    await db.commit()
    await db.refresh(delivery)
    return delivery


async def update(db: AsyncSession, delivery_id: int, data: DeliveryUpdate) -> Optional[Delivery]:
    delivery = await get_by_id(db, delivery_id)
    if not delivery:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(delivery, field, value)
    await db.commit()
    await db.refresh(delivery)
    return delivery


async def delete(db: AsyncSession, delivery_id: int) -> bool:
    delivery = await get_by_id(db, delivery_id)
    if not delivery:
        return False
    await db.delete(delivery)
    await db.commit()
    return True
