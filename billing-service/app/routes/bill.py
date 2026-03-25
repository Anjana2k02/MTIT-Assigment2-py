from fastapi import APIRouter, HTTPException
from app.schemas.bill import BillResponse
from app.services import bill_service

router = APIRouter(prefix="/bill", tags=["bill"])


@router.get("/{pos_order_id}", response_model=BillResponse)
async def get_bill(pos_order_id: str):
    """Generate a full bill breakdown for a POS order — subtotal, discount, tax, and total."""
    bill = await bill_service.get_bill(pos_order_id)
    if not bill:
        raise HTTPException(status_code=404, detail="POS order not found")
    return bill
