from fastapi import APIRouter, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="",
    tags=["store"],
    dependencies=[Security(require_bearer_token)],
)


@router.get("/store/")
async def get_store_items(request: Request):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/store/")


@router.post("/store/")
async def create_store_item(request: Request):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/store/")


@router.get("/store/{item_id}")
async def get_store_item(request: Request, item_id: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/store/{item_id}")


@router.put("/store/{item_id}")
async def update_store_item(request: Request, item_id: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/store/{item_id}")


@router.delete("/store/{item_id}")
async def delete_store_item(request: Request, item_id: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/store/{item_id}")
