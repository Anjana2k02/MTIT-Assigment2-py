from typing import Any, Dict

from fastapi import APIRouter, Body, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="",
    tags=["deliveries"],
    dependencies=[Security(require_bearer_token)],
)


@router.get("/deliveries/")
async def get_deliveries(request: Request):
    return await forward_request(request, f"{settings.DELIVERY_SERVICE_URL}/api/v1/deliveries/")


@router.post("/deliveries/")
async def create_delivery(
    request: Request,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "order_id": "ORDER_ID",
            "delivery_address": "123 Main Street",
            "delivery_status": "pending",
        },
    ),
):
    return await forward_request(request, f"{settings.DELIVERY_SERVICE_URL}/api/v1/deliveries/")


@router.get("/deliveries/{delivery_id}")
async def get_delivery(request: Request, delivery_id: str):
    return await forward_request(request, f"{settings.DELIVERY_SERVICE_URL}/api/v1/deliveries/{delivery_id}")


@router.put("/deliveries/{delivery_id}")
async def update_delivery(
    request: Request,
    delivery_id: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "delivery_status": "out_for_delivery",
            "notes": "Driver is on the way",
        },
    ),
):
    return await forward_request(request, f"{settings.DELIVERY_SERVICE_URL}/api/v1/deliveries/{delivery_id}")


@router.delete("/deliveries/{delivery_id}")
async def delete_delivery(request: Request, delivery_id: str):
    return await forward_request(request, f"{settings.DELIVERY_SERVICE_URL}/api/v1/deliveries/{delivery_id}")
