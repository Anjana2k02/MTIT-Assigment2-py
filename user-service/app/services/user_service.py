from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserSignUp, UserUpdate
from typing import List, Optional
import hashlib
import hmac
import secrets

PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 100_000
SALT_SIZE = 16

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(SALT_SIZE)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return f"{PBKDF2_ALGORITHM}${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash:
        return False
    try:
        algorithm, iterations_str, salt_hex, digest_hex = password_hash.split("$", 3)
        iterations = int(iterations_str)
        if algorithm != PBKDF2_ALGORITHM:
            return False
        expected = bytes.fromhex(digest_hex)
        computed = hashlib.pbkdf2_hmac(
            algorithm,
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            iterations,
        )
        return hmac.compare_digest(expected, computed)
    except (ValueError, TypeError):
        return False


def _ensure_default_role_id(db: Session) -> int:
    customer_role = db.query(Role).filter(Role.name == "customer").first()
    if customer_role:
        return customer_role.role_id

    first_role = db.query(Role).order_by(Role.role_id.asc()).first()
    if first_role:
        return first_role.role_id

    new_role = Role(name="customer", description="Default role for self-registered users")
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role.role_id

def create_user(db: Session, user: UserCreate) -> User:
    payload = user.dict(exclude={"password"})
    if payload.get("role_id") is None:
        payload["role_id"] = _ensure_default_role_id(db)
    payload["password_hash"] = hash_password(user.password)
    db_user = User(**payload)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def signup_user(db: Session, user: UserSignUp) -> User:
    create_payload = UserCreate(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    return create_user(db, create_payload)


def authenticate_user(db: Session, username: str, password: str) -> Optional[dict]:
    db_user = get_user_by_username(db, username)
    if not db_user or not verify_password(password, db_user.password_hash):
        return None

    role_name = "user"
    if db_user.role and db_user.role.name:
        role_name = db_user.role.name

    return {"username": db_user.username, "role": role_name}

def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    updates = user.dict(exclude_unset=True)
    password = updates.pop("password", None)
    if password:
        updates["password_hash"] = hash_password(password)
    for key, value in updates.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
