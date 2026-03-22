from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId
from app.models.billing import Invoice
from app.schemas.billing import InvoiceCreate, InvoiceUpdate


async def get_all() -> List[Invoice]:
    return await Invoice.find_all().to_list()


async def get_by_id(invoice_id: str) -> Optional[Invoice]:
    try:
        return await Invoice.get(PydanticObjectId(invoice_id))
    except Exception:
        return None


async def create(data: InvoiceCreate) -> Invoice:
    invoice = Invoice(**data.model_dump())
    await invoice.insert()
    return invoice


async def update(invoice_id: str, data: InvoiceUpdate) -> Optional[Invoice]:
    invoice = await get_by_id(invoice_id)
    if not invoice:
        return None
    update_data = data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    for field, value in update_data.items():
        setattr(invoice, field, value)
    await invoice.save()
    return invoice


async def delete(invoice_id: str) -> bool:
    invoice = await get_by_id(invoice_id)
    if not invoice:
        return False
    await invoice.delete()
    return True
