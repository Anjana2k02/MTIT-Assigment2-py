from beanie import Document


class Table(Document):
    location_id: str   # MongoDB ObjectId str of Location
    table_name: str
    status: int        # status_id (0, 1, 2) from TableStatus collection

    class Settings:
        name = "tables"
