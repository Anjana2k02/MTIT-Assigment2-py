from fastapi import APIRouter, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="",
    tags=["menu"],
    dependencies=[Security(require_bearer_token)],
)


@router.get("/menus/")
async def get_menus(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus/")


@router.post("/menus/")
async def create_menu(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus/")


@router.get("/menus/{menu_id}")
async def get_menu(request: Request, menu_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus/{menu_id}")


@router.put("/menus/{menu_id}")
async def update_menu(request: Request, menu_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus/{menu_id}")


@router.delete("/menus/{menu_id}")
async def delete_menu(request: Request, menu_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus/{menu_id}")


@router.get("/menus/{menu_id}/items")
async def get_items_in_menu(request: Request, menu_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus/{menu_id}/items")


@router.get("/items/")
async def get_items(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items/")


@router.post("/items/")
async def create_item(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items/")


@router.get("/items/{item_id}")
async def get_item(request: Request, item_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items/{item_id}")


@router.put("/items/{item_id}")
async def update_item(request: Request, item_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items/{item_id}")


@router.delete("/items/{item_id}")
async def delete_item(request: Request, item_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items/{item_id}")


@router.get("/menu-items/")
async def get_menu_items(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/")


@router.post("/menu-items/")
async def create_menu_item(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/")


@router.get("/menu-items/{menu_item_id}")
async def get_menu_item(request: Request, menu_item_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/{menu_item_id}")


@router.put("/menu-items/{menu_item_id}")
async def update_menu_item(request: Request, menu_item_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/{menu_item_id}")


@router.delete("/menu-items/{menu_item_id}")
async def delete_menu_item(request: Request, menu_item_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/{menu_item_id}")
