from typing import Any, Dict

from fastapi import APIRouter, Body, Request, Security
from app.auth.dependencies import require_bearer_token
from app.config import settings
from app.routes._proxy import forward_request

router = APIRouter(
    prefix="",
    tags=["tables"],
    dependencies=[Security(require_bearer_token)],
)


# locations
@router.get("/locations/")
async def get_locations(request: Request):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/locations/")


@router.post("/locations/")
async def create_location(
    request: Request,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "name": "Main Hall",
            "description": "Ground floor seating",
        },
    ),
):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/locations/")


@router.get("/locations/{location_id}")
async def get_location(request: Request, location_id: str):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/locations/{location_id}")


@router.put("/locations/{location_id}")
async def update_location(
    request: Request,
    location_id: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "name": "Updated Main Hall",
            "description": "Renovated seating area",
        },
    ),
):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/locations/{location_id}")


@router.delete("/locations/{location_id}")
async def delete_location(request: Request, location_id: str):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/locations/{location_id}")


@router.get("/locations/{location_id}/tables")
async def get_tables_in_location(request: Request, location_id: str):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/locations/{location_id}/tables")


# table-statuses
@router.get("/table-statuses/")
async def get_table_statuses(request: Request):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/table-statuses/")


@router.post("/table-statuses/")
async def create_table_status(
    request: Request,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "table_id": "TABLE_ID",
            "status": "available",
        },
    ),
):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/table-statuses/")


@router.get("/table-statuses/{status_doc_id}")
async def get_table_status(request: Request, status_doc_id: str):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/table-statuses/{status_doc_id}")


@router.put("/table-statuses/{status_doc_id}")
async def update_table_status(
    request: Request,
    status_doc_id: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "status": "occupied",
        },
    ),
):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/table-statuses/{status_doc_id}")


@router.delete("/table-statuses/{status_doc_id}")
async def delete_table_status(request: Request, status_doc_id: str):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/table-statuses/{status_doc_id}")


# tables
@router.get("/tables/")
async def get_tables(request: Request):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/tables/")


@router.post("/tables/")
async def create_table(
    request: Request,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "table_number": 12,
            "capacity": 4,
            "location_id": "LOCATION_ID",
        },
    ),
):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/tables/")


@router.get("/tables/{table_id}")
async def get_table(request: Request, table_id: str):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/tables/{table_id}")


@router.put("/tables/{table_id}")
async def update_table(
    request: Request,
    table_id: str,
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "capacity": 6,
            "is_active": True,
        },
    ),
):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/tables/{table_id}")


@router.delete("/tables/{table_id}")
async def delete_table(request: Request, table_id: str):
    return await forward_request(request, f"{settings.TABLE_SERVICE_URL}/api/v1/tables/{table_id}")
