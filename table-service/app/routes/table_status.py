from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.table_status import TableStatusCreate, TableStatusUpdate, TableStatusResponse
from app.services import table_status_service

router = APIRouter(prefix="/table-statuses", tags=["table-statuses"])


@router.get("/", response_model=List[TableStatusResponse])
async def get_table_statuses():
    return await table_status_service.get_all()


@router.get("/{status_doc_id}", response_model=TableStatusResponse)
async def get_table_status(status_doc_id: str):
    ts = await table_status_service.get_by_id(status_doc_id)
    if not ts:
        raise HTTPException(status_code=404, detail="Table status not found")
    return ts


@router.post("/", response_model=TableStatusResponse, status_code=201)
async def create_table_status(data: TableStatusCreate):
    return await table_status_service.create(data)


@router.put("/{status_doc_id}", response_model=TableStatusResponse)
async def update_table_status(status_doc_id: str, data: TableStatusUpdate):
    updated = await table_status_service.update(status_doc_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Table status not found")
    return updated


@router.delete("/{status_doc_id}", status_code=204)
async def delete_table_status(status_doc_id: str):
    deleted = await table_status_service.delete(status_doc_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Table status not found")
