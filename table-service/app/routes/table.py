from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.table import TableCreate, TableUpdate, TableResponse, TableDetailResponse
from app.services import table_service

router = APIRouter(prefix="/tables", tags=["tables"])

# Second router for nested /locations/{location_id}/tables endpoint
locations_router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=List[TableResponse])
async def get_tables():
    return await table_service.get_all()


@router.get("/{table_id}", response_model=TableResponse)
async def get_table(table_id: str):
    table = await table_service.get_by_id(table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table


@router.post("/", response_model=TableResponse, status_code=201)
async def create_table(data: TableCreate):
    created = await table_service.create(data)
    if not created:
        raise HTTPException(status_code=400, detail="Invalid status_id — no matching TableStatus found")
    return created


@router.put("/{table_id}", response_model=TableResponse)
async def update_table(table_id: str, data: TableUpdate):
    updated = await table_service.update(table_id, data)
    if updated is None:
        # distinguish: table not found vs invalid status
        existing = await table_service.get_by_id(table_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Table not found")
        raise HTTPException(status_code=400, detail="Invalid status_id — no matching TableStatus found")
    return updated


@router.delete("/{table_id}", status_code=204)
async def delete_table(table_id: str):
    deleted = await table_service.delete(table_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Table not found")


@locations_router.get("/{location_id}/tables", response_model=List[TableDetailResponse])
async def get_tables_in_location(location_id: str):
    return await table_service.get_tables_in_location(location_id)
