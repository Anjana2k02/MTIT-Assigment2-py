import motor.motor_asyncio
from beanie import init_beanie
from app.config import settings
from app.models.store import Store
from app.models.pos import POS



async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)

    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[Store, POS]
    )