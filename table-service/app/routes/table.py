from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.table import TableCreate, TableUpdate, TableResponse
from app.services import table_service

router = APIRouter(prefix="/tables", tags=["tables"])


@router.get("/", response_model=List[TableResponse])
async def get_tables(db: AsyncSession = Depends(get_db)):
    return await table_service.get_all(db)


@router.get("/{table_id}", response_model=TableResponse)
async def get_table(table_id: int, db: AsyncSession = Depends(get_db)):
    table = await table_service.get_by_id(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table


@router.post("/", response_model=TableResponse, status_code=201)
async def create_table(table: TableCreate, db: AsyncSession = Depends(get_db)):
    return await table_service.create(db, table)


@router.put("/{table_id}", response_model=TableResponse)
async def update_table(table_id: int, table: TableUpdate, db: AsyncSession = Depends(get_db)):
    updated = await table_service.update(db, table_id, table)
    if not updated:
        raise HTTPException(status_code=404, detail="Table not found")
    return updated


@router.delete("/{table_id}", status_code=204)
async def delete_table(table_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await table_service.delete(db, table_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Table not found")
