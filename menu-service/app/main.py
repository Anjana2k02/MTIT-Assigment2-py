from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import item as item_router
from app.routes import menu as menu_router
from app.routes import menu_item as menu_item_router
from app.config import settings
from app.database import init_db
from app.models.item import Item
from app.models.menu import Menu
from app.models.menu_item import MenuItem


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Item, Menu, MenuItem])
    yield


tags_metadata = [
    {"name": "items",      "description": "Manage individual food/drink items — name, price, type."},
    {"name": "menus",      "description": "Manage menu categories."},
    {"name": "menu-items", "description": "Link items to menus with availability control."},
    {"name": "health",     "description": "Service health check."},
]

app = FastAPI(
    title="Menu Service",
    description="Manages the restaurant menu — items, categories and availability.",
    version="2.0.0",
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

app.include_router(item_router.router,            prefix="/api/v1")
app.include_router(menu_router.router,            prefix="/api/v1")
app.include_router(menu_item_router.router,       prefix="/api/v1")
app.include_router(menu_item_router.menus_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
