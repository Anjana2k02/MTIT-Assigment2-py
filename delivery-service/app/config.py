from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "delivery-service"
    SERVICE_PORT: int = 8006
    DATABASE_URL: str = "sqlite+aiosqlite:///./delivery.db"

    class Config:
        env_file = ".env"


settings = Settings()
