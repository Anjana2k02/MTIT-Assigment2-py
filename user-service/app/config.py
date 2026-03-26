import os

DEFAULT_MONGODB_URL = "mongodb+srv://Admin:password@mtit.9eco5id.mongodb.net/restaurant?appName=mtit"

MONGODB_URL = os.getenv("MONGODB_URL") or DEFAULT_MONGODB_URL
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME") or "restaurant"
