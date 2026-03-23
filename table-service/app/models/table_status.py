from beanie import Document


class TableStatus(Document):
    status_id: int   # 0, 1, 2
    type: str        # 'available', 'Reserved', 'Not-Cleaned'

    class Settings:
        name = "table_statuses"
