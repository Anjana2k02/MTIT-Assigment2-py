from typing import Optional
from beanie import PydanticObjectId
from app.models.billing import PosOrder
from app.models.discount import Discount
from app.schemas.bill import BillResponse, BillItemDetail


async def get_bill(pos_order_id: str) -> Optional[BillResponse]:
    try:
        order = await PosOrder.get(PydanticObjectId(pos_order_id))
    except Exception:
        return None

    if not order:
        return None

    # Resolve discount
    discount_name = "no-discount"
    discount_percent = 0.0
    if order.discount_id:
        try:
            discount = await Discount.get(PydanticObjectId(order.discount_id))
            if discount:
                discount_name = discount.name
                discount_percent = discount.amount
        except Exception:
            pass

    discount_amount = round(order.subtotal * discount_percent / 100, 2)
    after_discount = round(order.subtotal - discount_amount, 2)

    return BillResponse(
        order_id=order.id,
        order_type=order.order_type,
        customer_name=order.customer_name,
        table_number=order.table_number,
        delivery_address=order.delivery_address,
        items=[
            BillItemDetail(
                item_id=item.item_id,
                name=item.name,
                price=item.price,
                quantity=item.quantity,
                subtotal=item.subtotal,
            )
            for item in order.items
        ],
        subtotal=order.subtotal,
        discount_name=discount_name,
        discount_percent=discount_percent,
        discount_amount=discount_amount,
        after_discount=after_discount,
        tax=order.tax,
        total=order.total,
        status=order.status,
        created_at=order.created_at,
    )
