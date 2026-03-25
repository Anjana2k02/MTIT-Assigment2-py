from typing import List, Optional
from beanie import PydanticObjectId
from app.models.table_status import TableStatus
from app.schemas.table_status import TableStatusCreate, TableStatusUpdate


async def get_all() -> List[TableStatus]:
    return await TableStatus.find_all().to_list()


async def get_by_id(status_doc_id: str) -> Optional[TableStatus]:
    try:
        return await TableStatus.get(PydanticObjectId(status_doc_id))
    except Exception:
        return None


async def get_by_status_id(status_id: int) -> Optional[TableStatus]:
    return await TableStatus.find_one(TableStatus.status_id == status_id)


async def create(data: TableStatusCreate) -> TableStatus:
    ts = TableStatus(**data.model_dump())
    await ts.insert()
    return ts


async def update(status_doc_id: str, data: TableStatusUpdate) -> Optional[TableStatus]:
    ts = await get_by_id(status_doc_id)
    if not ts:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(ts, field, value)
    await ts.save()
    return ts


async def delete(status_doc_id: str) -> bool:
    ts = await get_by_id(status_doc_id)
    if not ts:
        return False
    await ts.delete()
    return True
