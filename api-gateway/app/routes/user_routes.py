from typing import Any, Dict

from fastapi import APIRouter, Body, Request, Security

from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    tags=["users"],
    dependencies=[Security(require_bearer_token)],
)


@router.get("/users")
async def get_users_root(request: Request):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users")


@router.post("/users")
async def create_user_root(
    request: Request,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "name": "John Doe",
            "email": "john@example.com",
            "role": "staff",
        },
    ),
):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users")


@router.get("/users/{path:path}")
async def get_users_path(request: Request, path: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/{path}")


@router.post("/users/{path:path}")
async def post_users_path(
    request: Request,
    path: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "name": "John Doe",
            "email": "john@example.com",
        },
    ),
):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/{path}")


@router.put("/users/{path:path}")
async def put_users_path(
    request: Request,
    path: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "name": "Updated Name",
            "is_active": True,
        },
    ),
):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/{path}")


@router.patch("/users/{path:path}")
async def patch_users_path(
    request: Request,
    path: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "is_active": False,
        },
    ),
):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/{path}")


@router.delete("/users/{path:path}")
async def delete_users_path(request: Request, path: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/{path}")


@router.get("/roles")
async def get_roles_root(request: Request):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles")


@router.post("/roles")
async def create_roles_root(
    request: Request,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "name": "manager",
            "permissions": ["read", "write"],
        },
    ),
):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles")


@router.get("/roles/{path:path}")
async def get_roles_path(request: Request, path: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/{path}")


@router.post("/roles/{path:path}")
async def post_roles_path(
    request: Request,
    path: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "name": "supervisor",
            "permissions": ["read"],
        },
    ),
):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/{path}")


@router.put("/roles/{path:path}")
async def put_roles_path(
    request: Request,
    path: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "permissions": ["read", "write", "delete"],
        },
    ),
):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/{path}")


@router.patch("/roles/{path:path}")
async def patch_roles_path(
    request: Request,
    path: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "is_active": False,
        },
    ),
):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/{path}")


@router.delete("/roles/{path:path}")
async def delete_roles_path(request: Request, path: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/{path}")
