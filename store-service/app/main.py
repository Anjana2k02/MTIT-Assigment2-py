from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import store as store_router
from app.routes import store_routes as pos_router
from app.config import settings
from app.database import init_db
from app.models.store import Store
from app.models.pos import POS


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


tags_metadata = [
    {"name": "stores", "description": "Manage stores — create, view, update, and delete store locations."},
    {"name": "pos",    "description": "Manage POS terminals — each POS is linked to a store."},
    {"name": "health", "description": "Service health check."},
]

app = FastAPI(
    title="Store Service",
    description="Manages ingredient and supply inventory for the restaurant store.",
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

app.include_router(store_router.router, prefix="/api/v1")
app.include_router(pos_router.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
