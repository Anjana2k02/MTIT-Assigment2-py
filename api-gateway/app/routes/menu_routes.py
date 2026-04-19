from typing import Literal, Optional

from fastapi import APIRouter, Body, Request, Security
from pydantic import BaseModel
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request


class MenuCreateRequest(BaseModel):
    menu_name: str
    description: Optional[str] = None


class MenuUpdateRequest(BaseModel):
    menu_name: Optional[str] = None
    description: Optional[str] = None


class ItemCreateRequest(BaseModel):
    item_name: str
    item_price: float
    item_type: Literal["KOT", "BOT", "Other"]
    description: Optional[str] = None


class ItemUpdateRequest(BaseModel):
    item_name: Optional[str] = None
    item_price: Optional[float] = None
    item_type: Optional[Literal["KOT", "BOT", "Other"]] = None
    description: Optional[str] = None


class MenuItemCreateRequest(BaseModel):
    item_id: str
    menu_id: str
    availability: bool = True


class MenuItemUpdateRequest(BaseModel):
    availability: Optional[bool] = None

router = APIRouter(
    prefix="",
    tags=["menu"],
    dependencies=[Security(require_bearer_token)],
)


@router.get("/menus/")
async def get_menus(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus/")


@router.post("/menus/")
async def create_menu(
    request: Request,
    payload: MenuCreateRequest = Body(
        ...,
        example={
            "menu_name": "Lunch Specials",
            "description": "Weekday lunch menu",
        },
    ),
):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus/")


@router.get("/menus/{menu_id}")
async def get_menu(request: Request, menu_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menus/{menu_id}")


@router.put("/menus/{menu_id}")
async def update_menu(
    request: Request,
    menu_id: str,
    payload: MenuUpdateRequest = Body(
        ...,
        example={
            "menu_name": "Updated Lunch Specials",
            "description": "Updated weekday lunch menu",
        },
    ),
):
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
async def create_item(
    request: Request,
    payload: ItemCreateRequest = Body(
        ...,
        example={
            "item_name": "Masala Tea",
            "item_price": 120.0,
            "item_type": "KOT",
            "description": "Freshly brewed",
        },
    ),
):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items/")


@router.get("/items/{item_id}")
async def get_item(request: Request, item_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items/{item_id}")


@router.put("/items/{item_id}")
async def update_item(
    request: Request,
    item_id: str,
    payload: ItemUpdateRequest = Body(
        ...,
        example={
            "item_price": 140.0,
            "description": "Updated description",
        },
    ),
):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items/{item_id}")


@router.delete("/items/{item_id}")
async def delete_item(request: Request, item_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/items/{item_id}")


@router.get("/menu-items/")
async def get_menu_items(request: Request):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/")


@router.post("/menu-items/")
async def create_menu_item(
    request: Request,
    payload: MenuItemCreateRequest = Body(
        ...,
        example={
            "item_id": "ITEM_ID",
            "menu_id": "MENU_ID",
            "availability": True,
        },
    ),
):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/")


@router.get("/menu-items/{menu_item_id}")
async def get_menu_item(request: Request, menu_item_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/{menu_item_id}")


@router.put("/menu-items/{menu_item_id}")
async def update_menu_item(
    request: Request,
    menu_item_id: str,
    payload: MenuItemUpdateRequest = Body(
        ...,
        example={
            "availability": False,
        },
    ),
):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/{menu_item_id}")


@router.delete("/menu-items/{menu_item_id}")
async def delete_menu_item(request: Request, menu_item_id: str):
    return await forward_request(request, f"{settings.MENU_SERVICE_URL}/api/v1/menu-items/{menu_item_id}")
