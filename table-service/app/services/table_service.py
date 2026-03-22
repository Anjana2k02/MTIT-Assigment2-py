from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.table import Table
from app.schemas.table import TableCreate, TableUpdate


async def get_all(db: AsyncSession) -> List[Table]:
    result = await db.execute(select(Table))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, table_id: int) -> Optional[Table]:
    result = await db.execute(select(Table).where(Table.id == table_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: TableCreate) -> Table:
    table = Table(**data.model_dump())
    db.add(table)
    await db.commit()
    await db.refresh(table)
    return table


async def update(db: AsyncSession, table_id: int, data: TableUpdate) -> Optional[Table]:
    table = await get_by_id(db, table_id)
    if not table:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(table, field, value)
    await db.commit()
    await db.refresh(table)
    return table


async def delete(db: AsyncSession, table_id: int) -> bool:
    table = await get_by_id(db, table_id)
    if not table:
        return False
    await db.delete(table)
    await db.commit()
    return True
