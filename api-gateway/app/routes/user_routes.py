from fastapi import APIRouter, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(prefix="")


# --- Users ---

@router.post("/users/signup", tags=["users"])
async def signup_user(request: Request):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/signup")


@router.post("/users/signin", tags=["users"])
async def signin_user(request: Request):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/signin")


@router.get("/users/", tags=["users"], dependencies=[Security(require_bearer_token)])
async def get_users(request: Request):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/")


@router.post("/users/", tags=["users"], dependencies=[Security(require_bearer_token)])
async def create_user(request: Request):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/")


@router.get("/users/{user_id}", tags=["users"], dependencies=[Security(require_bearer_token)])
async def get_user(request: Request, user_id: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/{user_id}")


@router.put("/users/{user_id}", tags=["users"], dependencies=[Security(require_bearer_token)])
async def update_user(request: Request, user_id: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/{user_id}")


@router.delete("/users/{user_id}", tags=["users"], dependencies=[Security(require_bearer_token)])
async def delete_user(request: Request, user_id: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/users/{user_id}")


# --- Roles ---

@router.get("/roles/", tags=["roles"], dependencies=[Security(require_bearer_token)])
async def get_roles(request: Request):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/")


@router.post("/roles/", tags=["roles"], dependencies=[Security(require_bearer_token)])
async def create_role(request: Request):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/")


@router.get("/roles/{role_id}", tags=["roles"], dependencies=[Security(require_bearer_token)])
async def get_role(request: Request, role_id: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/{role_id}")


@router.put("/roles/{role_id}", tags=["roles"], dependencies=[Security(require_bearer_token)])
async def update_role(request: Request, role_id: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/{role_id}")


@router.delete("/roles/{role_id}", tags=["roles"], dependencies=[Security(require_bearer_token)])
async def delete_role(request: Request, role_id: str):
    return await forward_request(request, f"{settings.USER_SERVICE_URL}/roles/{role_id}")
