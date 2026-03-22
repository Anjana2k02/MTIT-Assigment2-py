from fastapi import APIRouter, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="/menu",
    tags=["menu"],
    dependencies=[Security(require_bearer_token)],
)


@router.api_route("", methods=["GET", "POST"])
async def proxy_menu_root(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu")


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_menu(request: Request, path: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu/{path}")
