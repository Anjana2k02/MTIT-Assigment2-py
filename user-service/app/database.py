from pymongo import MongoClient
from pymongo.database import Database

from .config import MONGO_DB_NAME, MONGODB_URL

client = MongoClient(MONGODB_URL)


def get_database() -> Database:
    return client[MONGO_DB_NAME]


def get_db():
    yield get_database()
