from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo.database import Database

from app.schemas.role import RoleCreate, RoleUpdate


def _serialize_role(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "role_id": str(doc["_id"]),
        "name": doc["name"],
        "description": doc.get("description"),
    }


def _parse_object_id(value: str) -> Optional[ObjectId]:
    if not ObjectId.is_valid(value):
        return None
    return ObjectId(value)


def get_role(db: Database, role_id: str) -> Optional[Dict[str, Any]]:
    oid = _parse_object_id(role_id)
    if not oid:
        return None
    doc = db["roles"].find_one({"_id": oid})
    return _serialize_role(doc) if doc else None


def get_roles(db: Database, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    docs = db["roles"].find().skip(skip).limit(limit)
    return [_serialize_role(doc) for doc in docs]


def create_role(db: Database, role: RoleCreate) -> Dict[str, Any]:
    result = db["roles"].insert_one(role.dict())
    created = db["roles"].find_one({"_id": result.inserted_id})
    return _serialize_role(created)


def update_role(db: Database, role_id: str, role: RoleUpdate) -> Optional[Dict[str, Any]]:
    oid = _parse_object_id(role_id)
    if not oid:
        return None
    updates = role.dict(exclude_unset=True)
    if not updates:
        doc = db["roles"].find_one({"_id": oid})
        return _serialize_role(doc) if doc else None
    db["roles"].update_one({"_id": oid}, {"$set": updates})
    doc = db["roles"].find_one({"_id": oid})
    return _serialize_role(doc) if doc else None


def delete_role(db: Database, role_id: str) -> bool:
    oid = _parse_object_id(role_id)
    if not oid:
        return False
    result = db["roles"].delete_one({"_id": oid})
    return result.deleted_count > 0
