from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "menu-service"
    SERVICE_PORT: int = 8002
    DATABASE_URL: str = "sqlite+aiosqlite:///./menu.db"

    class Config:
        env_file = ".env"


settings = Settings()
