from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.table import TableCreate, TableUpdate, TableResponse
from app.services import table_service

router = APIRouter(prefix="/tables", tags=["tables"])


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
async def create_table(table: TableCreate):
    return await table_service.create(table)


@router.put("/{table_id}", response_model=TableResponse)
async def update_table(table_id: str, table: TableUpdate):
    updated = await table_service.update(table_id, table)
    if not updated:
        raise HTTPException(status_code=404, detail="Table not found")
    return updated


@router.delete("/{table_id}", status_code=204)
async def delete_table(table_id: str):
    deleted = await table_service.delete(table_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Table not found")
