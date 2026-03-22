from fastapi import APIRouter, Request, Response
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.api_route("", methods=["GET", "POST"])
async def proxy_deliveries_root(request: Request):
    return await forward_request(request, f"{settings.DELIVERY_SERVICE_URL}/api/v1/deliveries")


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_deliveries(request: Request, path: str):
    return await forward_request(request, f"{settings.DELIVERY_SERVICE_URL}/api/v1/deliveries/{path}")
