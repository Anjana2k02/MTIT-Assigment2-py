from typing import Any, Dict

from fastapi import APIRouter, Body, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="",
    tags=["billing"],
    dependencies=[Security(require_bearer_token)],
)


# pos
@router.get("/pos/")
async def get_pos_orders(request: Request):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/pos/")


@router.get("/pos/delivery")
async def get_pos_delivery_orders(request: Request):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/pos/delivery")


@router.get("/pos/{order_id}")
async def get_pos_order(request: Request, order_id: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/pos/{order_id}")


@router.post("/pos/")
async def create_pos_order(
    request: Request,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "order_type": "dining",
            "customer_name": "Alex",
            "table_number": 4,
            "items": [{"item_id": "MENU_ITEM_ID", "quantity": 2}],
            "tax_rate": 0.1,
        },
    ),
):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/pos/")


@router.put("/pos/{order_id}")
async def update_pos_order(
    request: Request,
    order_id: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "payment_status": "paid",
            "discount_id": "DISCOUNT_ID",
        },
    ),
):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/pos/{order_id}")


@router.delete("/pos/{order_id}")
async def delete_pos_order(request: Request, order_id: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/pos/{order_id}")


# discounts
@router.get("/discounts/")
async def get_discounts(request: Request):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/discounts/")


@router.get("/discounts/{discount_id}")
async def get_discount(request: Request, discount_id: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/discounts/{discount_id}")


@router.post("/discounts/")
async def create_discount(
    request: Request,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "code": "NEWYEAR10",
            "discount_type": "percentage",
            "value": 10,
        },
    ),
):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/discounts/")


@router.put("/discounts/{discount_id}")
async def update_discount(
    request: Request,
    discount_id: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "value": 15,
            "is_active": True,
        },
    ),
):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/discounts/{discount_id}")


@router.delete("/discounts/{discount_id}")
async def delete_discount(request: Request, discount_id: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/discounts/{discount_id}")


# bill
@router.get("/bill/{pos_order_id}")
async def get_bill(request: Request, pos_order_id: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/bill/{pos_order_id}")


# backward-compatible legacy proxy path
@router.get("/billing/{path:path}")
async def legacy_billing_get(request: Request, path: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/billing/{path}")


@router.post("/billing/{path:path}")
async def legacy_billing_post(
    request: Request,
    path: str,
    payload: Dict[str, Any] = Body(...),
):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/billing/{path}")


@router.put("/billing/{path:path}")
async def legacy_billing_put(
    request: Request,
    path: str,
    payload: Dict[str, Any] = Body(...),
):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/billing/{path}")


@router.patch("/billing/{path:path}")
async def legacy_billing_patch(
    request: Request,
    path: str,
    payload: Dict[str, Any] = Body(...),
):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/billing/{path}")


@router.delete("/billing/{path:path}")
async def legacy_billing_delete(request: Request, path: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/billing/{path}")
