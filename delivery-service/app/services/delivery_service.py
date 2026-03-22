from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId
from app.models.delivery import Delivery
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate


async def get_all() -> List[Delivery]:
    return await Delivery.find_all().to_list()


async def get_by_id(delivery_id: str) -> Optional[Delivery]:
    try:
        return await Delivery.get(PydanticObjectId(delivery_id))
    except Exception:
        return None


async def create(data: DeliveryCreate) -> Delivery:
    delivery = Delivery(**data.model_dump())
    await delivery.insert()
    return delivery


async def update(delivery_id: str, data: DeliveryUpdate) -> Optional[Delivery]:
    delivery = await get_by_id(delivery_id)
    if not delivery:
        return None
    update_data = data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    for field, value in update_data.items():
        setattr(delivery, field, value)
    await delivery.save()
    return delivery


async def delete(delivery_id: str) -> bool:
    delivery = await get_by_id(delivery_id)
    if not delivery:
        return False
    await delivery.delete()
    return True
