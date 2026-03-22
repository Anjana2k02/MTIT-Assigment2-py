from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import order as order_router
from app.config import settings
from app.database import init_db
from app.models.order import Order


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Order])
    yield


tags_metadata = [
    {"name": "orders", "description": "Create, read, update and delete customer orders."},
    {"name": "health", "description": "Service health check."},
]

app = FastAPI(
    title="Order Service",
    description="Manages customer orders — status lifecycle from pending to delivered.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_router.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
