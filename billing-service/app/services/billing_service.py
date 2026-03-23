from typing import List, Optional
from datetime import datetime
import httpx
from beanie import PydanticObjectId
from app.models.billing import PosOrder, PosItem, OrderType
from app.models.discount import Discount
from app.schemas.billing import PosCreate, PosUpdate
from app.config import settings


async def _fetch_menu_item(item_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.MENU_SERVICE_URL}/api/v1/items/{item_id}",
            timeout=5.0,
        )
        resp.raise_for_status()
        return resp.json()


async def _get_discount_rate(discount_id: Optional[str]) -> float:
    """Return discount percentage (0–100). Returns 0.0 if no discount or not found."""
    if not discount_id:
        return 0.0
    try:
        discount = await Discount.get(PydanticObjectId(discount_id))
        return discount.amount if discount else 0.0
    except Exception:
        return 0.0


async def get_all() -> List[PosOrder]:
    return await PosOrder.find_all().to_list()


async def get_by_id(order_id: str) -> Optional[PosOrder]:
    try:
        return await PosOrder.get(PydanticObjectId(order_id))
    except Exception:
        return None


async def get_delivery_orders() -> List[PosOrder]:
    return await PosOrder.find(PosOrder.order_type == OrderType.DELIVERY).to_list()


async def create(data: PosCreate) -> PosOrder:
    pos_items: List[PosItem] = []
    subtotal = 0.0

    for req in data.items:
        menu_item = await _fetch_menu_item(req.item_id)
        price: float = menu_item["item_price"]
        line_total = round(price * req.quantity, 2)
        pos_items.append(PosItem(
            item_id=req.item_id,
            name=menu_item["item_name"],
            price=price,
            quantity=req.quantity,
            subtotal=line_total,
        ))
        subtotal += line_total

    subtotal = round(subtotal, 2)
    discount_rate = await _get_discount_rate(data.discount_id)
    discount_amount = round(subtotal * discount_rate / 100, 2)
    after_discount = round(subtotal - discount_amount, 2)
    tax = round(after_discount * data.tax_rate, 2)
    total = round(after_discount + tax, 2)

    order = PosOrder(
        order_type=data.order_type,
        customer_name=data.customer_name,
        table_number=data.table_number,
        delivery_address=data.delivery_address,
        items=pos_items,
        discount_id=data.discount_id,
        subtotal=subtotal,
        tax=tax,
        total=total,
    )
    await order.insert()
    return order


async def update(order_id: str, data: PosUpdate) -> Optional[PosOrder]:
    order = await get_by_id(order_id)
    if not order:
        return None

    update_data = data.model_dump(exclude_unset=True)
    tax_rate = update_data.pop("tax_rate", None)

    for field, value in update_data.items():
        setattr(order, field, value)

    # Recalculate totals if discount or tax_rate changed
    if "discount_id" in update_data or tax_rate is not None:
        discount_rate = await _get_discount_rate(order.discount_id)
        discount_amount = round(order.subtotal * discount_rate / 100, 2)
        after_discount = round(order.subtotal - discount_amount, 2)
        current_tax_rate = tax_rate if tax_rate is not None else (order.tax / order.subtotal if order.subtotal else 0.0)
        order.tax = round(after_discount * current_tax_rate, 2)
        order.total = round(after_discount + order.tax, 2)

    order.updated_at = datetime.utcnow()
    await order.save()
    return order


async def delete(order_id: str) -> bool:
    order = await get_by_id(order_id)
    if not order:
        return False
    await order.delete()
    return True
