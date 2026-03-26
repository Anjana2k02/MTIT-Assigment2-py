import os

DEFAULT_DATABASE_URL = "sqlite:///./user.db"

DATABASE_URL = os.getenv("DATABASE_URL") or DEFAULT_DATABASE_URL
