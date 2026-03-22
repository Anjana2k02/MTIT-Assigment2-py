from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate


async def get_all() -> List[Order]:
    return await Order.find_all().to_list()


async def get_by_id(order_id: str) -> Optional[Order]:
    try:
        return await Order.get(PydanticObjectId(order_id))
    except Exception:
        return None


async def create(data: OrderCreate) -> Order:
    order = Order(**data.model_dump())
    await order.insert()
    return order


async def update(order_id: str, data: OrderUpdate) -> Optional[Order]:
    order = await get_by_id(order_id)
    if not order:
        return None
    update_data = data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    for field, value in update_data.items():
        setattr(order, field, value)
    await order.save()
    return order


async def delete(order_id: str) -> bool:
    order = await get_by_id(order_id)
    if not order:
        return False
    await order.delete()
    return True
