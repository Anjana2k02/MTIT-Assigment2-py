from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.billing import Invoice
from app.schemas.billing import InvoiceCreate, InvoiceUpdate


async def get_all(db: AsyncSession) -> List[Invoice]:
    result = await db.execute(select(Invoice))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, invoice_id: int) -> Optional[Invoice]:
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: InvoiceCreate) -> Invoice:
    invoice = Invoice(**data.model_dump())
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice


async def update(db: AsyncSession, invoice_id: int, data: InvoiceUpdate) -> Optional[Invoice]:
    invoice = await get_by_id(db, invoice_id)
    if not invoice:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(invoice, field, value)
    await db.commit()
    await db.refresh(invoice)
    return invoice


async def delete(db: AsyncSession, invoice_id: int) -> bool:
    invoice = await get_by_id(db, invoice_id)
    if not invoice:
        return False
    await db.delete(invoice)
    await db.commit()
    return True
