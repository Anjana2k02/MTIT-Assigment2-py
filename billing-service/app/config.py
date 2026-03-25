from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "pos-service"
    SERVICE_PORT: int = 8003
    MONGODB_URL: str = "mongodb+srv://Admin:password@mtit.9eco5id.mongodb.net/restaurant?appName=mtit"
    MONGO_DB_NAME: str = "restaurant"
    MENU_SERVICE_URL: str = "http://localhost:8002"

    class Config:
        env_file = ".env"


settings = Settings()
