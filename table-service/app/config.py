from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "table-service"
    SERVICE_PORT: int = 8004
    DATABASE_URL: str = "sqlite+aiosqlite:///./table.db"

    class Config:
        env_file = ".env"


settings = Settings()
