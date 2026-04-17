from fastapi import APIRouter, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="",
    tags=["orders"],
    dependencies=[Security(require_bearer_token)],
)


@router.get("/orders/")
async def get_orders(request: Request):
    return await forward_request(request, f"{settings.ORDER_SERVICE_URL}/api/v1/orders/")


@router.post("/orders/")
async def create_order(request: Request):
    return await forward_request(request, f"{settings.ORDER_SERVICE_URL}/api/v1/orders/")


@router.get("/orders/{order_id}")
async def get_order(request: Request, order_id: str):
    return await forward_request(request, f"{settings.ORDER_SERVICE_URL}/api/v1/orders/{order_id}")


@router.put("/orders/{order_id}")
async def update_order(request: Request, order_id: str):
    return await forward_request(request, f"{settings.ORDER_SERVICE_URL}/api/v1/orders/{order_id}")


@router.delete("/orders/{order_id}")
async def delete_order(request: Request, order_id: str):
    return await forward_request(request, f"{settings.ORDER_SERVICE_URL}/api/v1/orders/{order_id}")
