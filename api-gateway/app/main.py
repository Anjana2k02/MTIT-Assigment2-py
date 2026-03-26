from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth_routes,
    order_routes,
    menu_routes,
    billing_routes,
    table_routes,
    store_routes,
    delivery_routes,
)
from app.middleware.logging import LoggingMiddleware
from app.config import settings
import httpx

tags_metadata = [
    {"name": "auth",       "description": "Gateway authentication endpoints"},
    {"name": "orders",     "description": "Proxy → Order Service :8001"},
    {"name": "menu",       "description": "Proxy → Menu Service :8002"},
    {"name": "billing",    "description": "Proxy → Billing Service :8003"},
    {"name": "tables",     "description": "Proxy → Table Service :8004"},
    {"name": "stores",     "description": "Proxy → Store Service :8005"},
    {"name": "pos",        "description": "Proxy → Store Service :8005 — POS terminals"},
    {"name": "deliveries", "description": "Proxy → Delivery Service :8006"},
    {"name": "gateway",    "description": "Gateway health & downstream status"},
]

app = FastAPI(
    title="API Gateway",
    description="Central entry point — routes all requests to downstream microservices.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

app.include_router(auth_routes.router)
app.include_router(order_routes.router, prefix="/api/v1")
app.include_router(menu_routes.router, prefix="/api/v1")
app.include_router(billing_routes.router, prefix="/api/v1")
app.include_router(table_routes.router, prefix="/api/v1")
app.include_router(store_routes.router, prefix="/api/v1")
app.include_router(delivery_routes.router, prefix="/api/v1")


@app.get("/health", tags=["gateway"])
async def health():
    service_urls = {
        "order": settings.ORDER_SERVICE_URL,
        "menu": settings.MENU_SERVICE_URL,
        "billing": settings.BILLING_SERVICE_URL,
        "table": settings.TABLE_SERVICE_URL,
        "store": settings.STORE_SERVICE_URL,
        "delivery": settings.DELIVERY_SERVICE_URL,
    }
    statuses = {}
    async with httpx.AsyncClient(timeout=3.0) as client:
        for name, url in service_urls.items():
            try:
                resp = await client.get(f"{url}/health")
                statuses[name] = "healthy" if resp.status_code == 200 else "unhealthy"
            except Exception:
                statuses[name] = "unreachable"
    return {"gateway": "healthy", "services": statuses}
