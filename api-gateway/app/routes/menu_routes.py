from fastapi import APIRouter, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="",
    tags=["menu"],
    dependencies=[Security(require_bearer_token)],
)


@router.api_route("/menus", methods=["GET", "POST"])
async def proxy_menus_root(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus")


@router.api_route("/menus/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_menus(request: Request, path: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus/{path}")


@router.api_route("/items", methods=["GET", "POST"])
async def proxy_items_root(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items")


@router.api_route("/items/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_items(request: Request, path: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items/{path}")


@router.api_route("/menu-items", methods=["GET", "POST"])
async def proxy_menu_items_root(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items")


@router.api_route("/menu-items/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_menu_items(request: Request, path: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/{path}")
