from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "billing-service"
    SERVICE_PORT: int = 8003
    DATABASE_URL: str = "sqlite+aiosqlite:///./billing.db"

    class Config:
        env_file = ".env"


settings = Settings()
