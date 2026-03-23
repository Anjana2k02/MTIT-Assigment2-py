import enum
from beanie import Document
from pydantic import Field


class TableStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"


class Table(Document):
    location_id: str
    table_name: str
    status_id: str

    class Settings:
        name = "tables"
