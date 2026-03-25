from typing import List, Optional
from beanie import PydanticObjectId
from app.models.store import Store
from app.schemas.store import StoreCreate, StoreUpdate


async def get_all() -> List[Store]:
    return await Store.find_all().to_list()


async def get_by_id(store_id: str) -> Optional[Store]:
    try:
        return await Store.get(PydanticObjectId(store_id))
    except Exception:
        return None


async def create(data: StoreCreate) -> Store:
    store = Store(**data.model_dump())
    await store.insert()
    return store


async def update(store_id: str, data: StoreUpdate) -> Optional[Store]:
    store = await get_by_id(store_id)
    if not store:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(store, field, value)

    await store.save()
    return store


async def delete(store_id: str) -> bool:
    store = await get_by_id(store_id)
    if not store:
        return False

    await store.delete()
    return True