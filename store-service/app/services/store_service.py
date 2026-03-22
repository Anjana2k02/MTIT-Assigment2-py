from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId
from app.models.store import StoreItem
from app.schemas.store import StoreItemCreate, StoreItemUpdate


async def get_all() -> List[StoreItem]:
    return await StoreItem.find_all().to_list()


async def get_by_id(item_id: str) -> Optional[StoreItem]:
    try:
        return await StoreItem.get(PydanticObjectId(item_id))
    except Exception:
        return None


async def create(data: StoreItemCreate) -> StoreItem:
    item = StoreItem(**data.model_dump())
    await item.insert()
    return item


async def update(item_id: str, data: StoreItemUpdate) -> Optional[StoreItem]:
    item = await get_by_id(item_id)
    if not item:
        return None
    update_data = data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    for field, value in update_data.items():
        setattr(item, field, value)
    await item.save()
    return item


async def delete(item_id: str) -> bool:
    item = await get_by_id(item_id)
    if not item:
        return False
    await item.delete()
    return True
