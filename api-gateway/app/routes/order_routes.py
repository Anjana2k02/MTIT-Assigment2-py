from fastapi import APIRouter, Request, Response
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(prefix="/orders", tags=["orders"])


@router.api_route("", methods=["GET", "POST"])
async def proxy_orders_root(request: Request):
    return await forward_request(request, f"{settings.ORDER_SERVICE_URL}/api/v1/orders")


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_orders(request: Request, path: str):
    return await forward_request(request, f"{settings.ORDER_SERVICE_URL}/api/v1/orders/{path}")
