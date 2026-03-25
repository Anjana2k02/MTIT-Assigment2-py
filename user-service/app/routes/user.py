from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserCreate, UserSignIn, UserSignInOut, UserSignUp, UserUpdate, UserOut
from app.services.user_service import (
    authenticate_user,
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    get_user_by_username,
    get_users,
    signup_user,
    update_user,
)
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=UserOut, status_code=201)
def signup(user: UserSignUp, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="Email already exists")
    return signup_user(db, user)


@router.post("/signin", response_model=UserSignInOut)
def signin(payload: UserSignIn, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="Email already exists")
    return create_user(db, user)

@router.put("/{user_id}", response_model=UserOut)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}
