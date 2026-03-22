from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.billing import InvoiceCreate, InvoiceUpdate, InvoiceResponse
from app.services import billing_service

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices(db: AsyncSession = Depends(get_db)):
    return await billing_service.get_all(db)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
    invoice = await billing_service.get_by_id(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/", response_model=InvoiceResponse, status_code=201)
async def create_invoice(invoice: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    return await billing_service.create(db, invoice)


@router.put("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(invoice_id: int, invoice: InvoiceUpdate, db: AsyncSession = Depends(get_db)):
    updated = await billing_service.update(db, invoice_id, invoice)
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return updated


@router.delete("/{invoice_id}", status_code=204)
async def delete_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await billing_service.delete(db, invoice_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Invoice not found")
