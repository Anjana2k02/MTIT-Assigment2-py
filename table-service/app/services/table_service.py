from typing import List, Optional
from beanie import PydanticObjectId
from app.models.table import Table
from app.models.table_status import TableStatus
from app.schemas.table import TableCreate, TableUpdate, TableDetailResponse


async def get_all() -> List[Table]:
    return await Table.find_all().to_list()


async def get_by_id(table_id: str) -> Optional[Table]:
    try:
        return await Table.get(PydanticObjectId(table_id))
    except Exception:
        return None


async def status_exists(status_id: int) -> bool:
    result = await TableStatus.find_one(TableStatus.status_id == status_id)
    return result is not None


async def create(data: TableCreate) -> Optional[Table]:
    if not await status_exists(data.status):
        return None
    table = Table(**data.model_dump())
    await table.insert()
    return table


async def update(table_id: str, data: TableUpdate) -> Optional[Table]:
    table = await get_by_id(table_id)
    if not table:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if 'status' in update_data and not await status_exists(update_data['status']):
        return None
    for field, value in update_data.items():
        setattr(table, field, value)
    await table.save()
    return table


async def delete(table_id: str) -> bool:
    table = await get_by_id(table_id)
    if not table:
        return False
    await table.delete()
    return True


async def get_tables_in_location(location_id: str) -> List[TableDetailResponse]:
    tables = await Table.find(Table.location_id == location_id).to_list()
    results = []
    for t in tables:
        status_doc: Optional[TableStatus] = None
        try:
            status_doc = await TableStatus.find_one(TableStatus.status_id == t.status)
        except Exception:
            pass
        results.append(
            TableDetailResponse(
                id=str(t.id),
                location_id=t.location_id,
                table_name=t.table_name,
                status=t.status,
                status_detail=status_doc,
            )
        )
    return results
