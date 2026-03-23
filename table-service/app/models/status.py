from enum import Enum

class StatusType(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    NOT_CLEANED = "not_cleaned"