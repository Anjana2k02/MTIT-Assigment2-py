from typing import List, Optional
from beanie import PydanticObjectId
from app.models.pos import POS
from app.schemas.pos import POSCreate, POSUpdate


async def get_all() -> List[POS]:
    return await POS.find_all().to_list()


async def get_by_id(pos_id: str) -> Optional[POS]:
    try:
        return await POS.get(PydanticObjectId(pos_id))
    except Exception:
        return None


async def get_by_store_id(store_id: str) -> List[POS]:
    return await POS.find(POS.store_id == store_id).to_list()


async def create(data: POSCreate) -> POS:
    pos = POS(**data.model_dump())
    await pos.insert()
    return pos


async def update(pos_id: str, data: POSUpdate) -> Optional[POS]:
    pos = await get_by_id(pos_id)
    if not pos:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pos, field, value)

    await pos.save()
    return pos


async def delete(pos_id: str) -> bool:
    pos = await get_by_id(pos_id)
    if not pos:
        return False

    await pos.delete()
    return True