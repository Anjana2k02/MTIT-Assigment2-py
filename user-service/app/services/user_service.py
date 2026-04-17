from typing import Any, Dict, List, Optional
import hashlib
import hmac
import secrets

from bson import ObjectId
from pymongo.database import Database

from app.schemas.user import UserCreate, UserSignUp, UserUpdate

PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 100_000
SALT_SIZE = 16

def _serialize_user(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "user_id": str(doc["_id"]),
        "username": doc["username"],
        "email": doc["email"],
        "address": doc.get("address"),
        "phoneNo": doc.get("phoneNo"),
        "role_id": str(doc["role_id"]) if doc.get("role_id") else None,
    }


def _parse_object_id(value: str) -> Optional[ObjectId]:
    if not ObjectId.is_valid(value):
        return None
    return ObjectId(value)


def get_user(db: Database, user_id: str) -> Optional[Dict[str, Any]]:
    oid = _parse_object_id(user_id)
    if not oid:
        return None
    doc = db["users"].find_one({"_id": oid})
    return _serialize_user(doc) if doc else None


def get_user_by_username(db: Database, username: str) -> Optional[Dict[str, Any]]:
    doc = db["users"].find_one({"username": username})
    return _serialize_user(doc) if doc else None


def get_user_by_email(db: Database, email: str) -> Optional[Dict[str, Any]]:
    doc = db["users"].find_one({"email": email})
    return _serialize_user(doc) if doc else None


def get_users(db: Database, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    docs = db["users"].find().skip(skip).limit(limit)
    return [_serialize_user(doc) for doc in docs]


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


def _ensure_default_role_id(db: Database) -> ObjectId:
    customer_role = db["roles"].find_one({"name": "customer"})
    if customer_role:
        return customer_role["_id"]

    first_role = db["roles"].find_one(sort=[("_id", 1)])
    if first_role:
        return first_role["_id"]

    role_insert = db["roles"].insert_one(
        {"name": "customer", "description": "Default role for self-registered users"}
    )
    return role_insert.inserted_id


def create_user(db: Database, user: UserCreate) -> Dict[str, Any]:
    payload = user.dict(exclude={"password"})
    if payload.get("role_id") is None:
        payload["role_id"] = _ensure_default_role_id(db)
    else:
        role_oid = _parse_object_id(payload["role_id"])
        if not role_oid:
            payload["role_id"] = _ensure_default_role_id(db)
        else:
            payload["role_id"] = role_oid
    payload["password_hash"] = hash_password(user.password)
    result = db["users"].insert_one(payload)
    created = db["users"].find_one({"_id": result.inserted_id})
    return _serialize_user(created)


def signup_user(db: Database, user: UserSignUp) -> Dict[str, Any]:
    create_payload = UserCreate(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    return create_user(db, create_payload)


def authenticate_user(db: Database, username: str, password: str) -> Optional[dict]:
    db_user = db["users"].find_one({"username": username})
    if not db_user or not verify_password(password, db_user.get("password_hash")):
        return None

    role_name = "user"
    role_id = db_user.get("role_id")
    if role_id:
        role_doc = db["roles"].find_one({"_id": role_id})
        if role_doc and role_doc.get("name"):
            role_name = role_doc["name"]

    return {"username": db_user["username"], "role": role_name}

def update_user(db: Database, user_id: str, user: UserUpdate) -> Optional[Dict[str, Any]]:
    oid = _parse_object_id(user_id)
    if not oid:
        return None
    updates = user.dict(exclude_unset=True)
    password = updates.pop("password", None)
    if password:
        updates["password_hash"] = hash_password(password)
    if "role_id" in updates and updates["role_id"] is not None:
        role_oid = _parse_object_id(updates["role_id"])
        if not role_oid:
            return None
        updates["role_id"] = role_oid

    db["users"].update_one({"_id": oid}, {"$set": updates})
    doc = db["users"].find_one({"_id": oid})
    return _serialize_user(doc) if doc else None

def delete_user(db: Database, user_id: str) -> bool:
    oid = _parse_object_id(user_id)
    if not oid:
        return False
    result = db["users"].delete_one({"_id": oid})
    return result.deleted_count > 0
