from fastapi import APIRouter, Request, Security
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
async def create_pos_order(request: Request):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/pos/")


@router.put("/pos/{order_id}")
async def update_pos_order(request: Request, order_id: str):
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
async def create_discount(request: Request):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/discounts/")


@router.put("/discounts/{discount_id}")
async def update_discount(request: Request, discount_id: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/discounts/{discount_id}")


@router.delete("/discounts/{discount_id}")
async def delete_discount(request: Request, discount_id: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/discounts/{discount_id}")


# bill
@router.get("/bill/{pos_order_id}")
async def get_bill(request: Request, pos_order_id: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/bill/{pos_order_id}")


# backward-compatible legacy proxy path
@router.api_route("/billing/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_legacy_billing(request: Request, path: str):
    return await forward_request(request, f"{settings.BILLING_SERVICE_URL}/api/v1/billing/{path}")
