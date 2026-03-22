from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.billing import InvoiceCreate, InvoiceUpdate, InvoiceResponse
from app.services import billing_service

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices():
    return await billing_service.get_all()


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: str):
    invoice = await billing_service.get_by_id(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/", response_model=InvoiceResponse, status_code=201)
async def create_invoice(invoice: InvoiceCreate):
    return await billing_service.create(invoice)


@router.put("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(invoice_id: str, invoice: InvoiceUpdate):
    updated = await billing_service.update(invoice_id, invoice)
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return updated


@router.delete("/{invoice_id}", status_code=204)
async def delete_invoice(invoice_id: str):
    deleted = await billing_service.delete(invoice_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Invoice not found")
