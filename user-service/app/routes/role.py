from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut
from app.services.role_service import get_role, get_roles, create_role, update_role, delete_role
from app.database import get_db

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=List[RoleOut])
def read_roles(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return get_roles(db, skip=skip, limit=limit)

@router.get("/{role_id}", response_model=RoleOut)
def read_role(role_id: str, db=Depends(get_db)):
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.post("/", response_model=RoleOut)
def create_new_role(role: RoleCreate, db=Depends(get_db)):
    return create_role(db, role)

@router.put("/{role_id}", response_model=RoleOut)
def update_existing_role(role_id: str, role: RoleUpdate, db=Depends(get_db)):
    db_role = update_role(db, role_id, role)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.delete("/{role_id}")
def delete_existing_role(role_id: str, db=Depends(get_db)):
    success = delete_role(db, role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"ok": True}
