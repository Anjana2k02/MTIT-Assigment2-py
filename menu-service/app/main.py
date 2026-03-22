from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import menu as menu_router
from app.config import settings
from app.database import init_db
from app.models.menu import MenuItem


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([MenuItem])
    yield


tags_metadata = [
    {"name": "menu",   "description": "Manage menu items — name, price, category, availability."},
    {"name": "health", "description": "Service health check."},
]

app = FastAPI(
    title="Menu Service",
    description="Manages the restaurant menu — items, prices, categories and availability.",
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

app.include_router(menu_router.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
