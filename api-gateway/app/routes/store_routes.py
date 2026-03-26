from fastapi import APIRouter, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="",
    dependencies=[Security(require_bearer_token)],
)


# --- Stores ---

@router.get("/stores/", tags=["stores"])
async def get_stores(request: Request):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/stores/")


@router.post("/stores/", tags=["stores"])
async def create_store(request: Request):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/stores/")


@router.get("/stores/{store_id}", tags=["stores"])
async def get_store(request: Request, store_id: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/stores/{store_id}")


@router.put("/stores/{store_id}", tags=["stores"])
async def update_store(request: Request, store_id: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/stores/{store_id}")


@router.delete("/stores/{store_id}", tags=["stores"])
async def delete_store(request: Request, store_id: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/stores/{store_id}")


# --- POS Terminals ---

@router.get("/pos/", tags=["pos"])
async def get_pos_list(request: Request):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/pos/")


@router.post("/pos/", tags=["pos"])
async def create_pos(request: Request):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/pos/")


@router.get("/pos/store/{store_id}", tags=["pos"])
async def get_pos_by_store(request: Request, store_id: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/pos/store/{store_id}")


@router.get("/pos/{pos_id}", tags=["pos"])
async def get_pos(request: Request, pos_id: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/pos/{pos_id}")


@router.put("/pos/{pos_id}", tags=["pos"])
async def update_pos(request: Request, pos_id: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/pos/{pos_id}")


@router.delete("/pos/{pos_id}", tags=["pos"])
async def delete_pos(request: Request, pos_id: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/pos/{pos_id}")
