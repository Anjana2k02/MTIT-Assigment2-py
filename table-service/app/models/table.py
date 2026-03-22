import enum
from beanie import Document


class TableStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"


class Table(Document):
    table_number: int
    capacity: int
    status: TableStatus = TableStatus.AVAILABLE

    class Settings:
        name = "tables"
