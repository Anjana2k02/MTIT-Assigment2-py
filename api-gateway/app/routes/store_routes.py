from fastapi import APIRouter, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="/store",
    tags=["store"],
    dependencies=[Security(require_bearer_token)],
)


@router.api_route("", methods=["GET", "POST"])
async def proxy_store_root(request: Request):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/store")


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_store(request: Request, path: str):
    return await forward_request(request, f"{settings.STORE_SERVICE_URL}/api/v1/store/{path}")
