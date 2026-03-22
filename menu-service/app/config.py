from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "menu-service"
    SERVICE_PORT: int = 8002
    MONGODB_URL: str = "mongodb+srv://Admin:password@mtit.9eco5id.mongodb.net/restaurant?appName=mtit"
    MONGO_DB_NAME: str = "restaurant"

    class Config:
        env_file = ".env"


settings = Settings()
