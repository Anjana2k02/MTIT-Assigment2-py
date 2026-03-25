from fastapi import APIRouter, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Security(require_bearer_token)],
)

@router.api_route("", methods=["GET", "POST"])
async def proxy_users_root(request: Request):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users")

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_users(request: Request, path: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/{path}")

@router.api_route("/roles", methods=["GET", "POST"])
async def proxy_roles_root(request: Request):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles")

@router.api_route("/roles/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_roles(request: Request, path: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/{path}")
