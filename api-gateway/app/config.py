from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ORDER_SERVICE_URL: str = "http://localhost:8001"
    MENU_SERVICE_URL: str = "http://localhost:8002"
    BILLING_SERVICE_URL: str = "http://localhost:8003"
    TABLE_SERVICE_URL: str = "http://localhost:8004"
    STORE_SERVICE_URL: str = "http://localhost:8005"
    DELIVERY_SERVICE_URL: str = "http://localhost:8006"
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
