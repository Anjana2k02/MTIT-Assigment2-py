from typing import List, Optional
from beanie import PydanticObjectId
from app.models.table import Table
from app.schemas.table import TableCreate, TableUpdate


async def get_all() -> List[Table]:
    return await Table.find_all().to_list()


async def get_by_id(table_id: str) -> Optional[Table]:
    try:
        return await Table.get(PydanticObjectId(table_id))
    except Exception:
        return None


async def create(data: TableCreate) -> Table:
    table = Table(**data.model_dump())
    await table.insert()
    return table


async def update(table_id: str, data: TableUpdate) -> Optional[Table]:
    table = await get_by_id(table_id)
    if not table:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(table, field, value)
    await table.save()
    return table


async def delete(table_id: str) -> bool:
    table = await get_by_id(table_id)
    if not table:
        return False
    await table.delete()
    return True
