from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ORDER_SERVICE_URL: str = "http://order-service:8001"
    MENU_SERVICE_URL: str = "http://menu-service:8002"
    BILLING_SERVICE_URL: str = "http://billing-service:8003"
    TABLE_SERVICE_URL: str = "http://table-service:8004"
    STORE_SERVICE_URL: str = "http://store-service:8005"
    DELIVERY_SERVICE_URL: str = "http://delivery-service:8006"

    class Config:
        env_file = ".env"


settings = Settings()
