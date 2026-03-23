from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId
from app.models.discount import Discount
from app.schemas.discount import DiscountCreate, DiscountUpdate


async def get_all() -> List[Discount]:
    return await Discount.find_all().to_list()


async def get_by_id(discount_id: str) -> Optional[Discount]:
    try:
        return await Discount.get(PydanticObjectId(discount_id))
    except Exception:
        return None


async def create(data: DiscountCreate) -> Discount:
    discount = Discount(**data.model_dump())
    await discount.insert()
    return discount


async def update(discount_id: str, data: DiscountUpdate) -> Optional[Discount]:
    discount = await get_by_id(discount_id)
    if not discount:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(discount, field, value)
    await discount.save()
    return discount


async def delete(discount_id: str) -> bool:
    discount = await get_by_id(discount_id)
    if not discount:
        return False
    await discount.delete()
    return True
