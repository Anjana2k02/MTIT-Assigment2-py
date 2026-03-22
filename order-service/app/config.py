from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "order-service"
    SERVICE_PORT: int = 8001
    DATABASE_URL: str = "sqlite+aiosqlite:///./order.db"

    class Config:
        env_file = ".env"


settings = Settings()
