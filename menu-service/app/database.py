import motor.motor_asyncio
from beanie import init_beanie
from app.config import settings


async def init_db(document_models: list):
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client[settings.MONGO_DB_NAME], document_models=document_models)
