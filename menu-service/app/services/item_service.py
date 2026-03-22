from typing import List, Optional
from beanie import PydanticObjectId
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


async def get_all() -> List[Item]:
    return await Item.find_all().to_list()


async def get_by_id(item_id: str) -> Optional[Item]:
    try:
        return await Item.get(PydanticObjectId(item_id))
    except Exception:
        return None


async def create(data: ItemCreate) -> Item:
    item = Item(**data.model_dump())
    await item.insert()
    return item


async def update(item_id: str, data: ItemUpdate) -> Optional[Item]:
    item = await get_by_id(item_id)
    if not item:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await item.save()
    return item


async def delete(item_id: str) -> bool:
    item = await get_by_id(item_id)
    if not item:
        return False
    await item.delete()
    return True
