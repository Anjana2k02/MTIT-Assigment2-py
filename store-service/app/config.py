from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "store-service"
    SERVICE_PORT: int = 8005
    DATABASE_URL: str = "sqlite+aiosqlite:///./store.db"

    class Config:
        env_file = ".env"


settings = Settings()
