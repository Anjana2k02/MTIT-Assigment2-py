from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import table as table_router
from app.config import settings
from app.database import init_db
from app.models.table import Table


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Table])
    yield


tags_metadata = [
    {"name": "tables", "description": "Manage restaurant tables — capacity and availability status."},
    {"name": "health", "description": "Service health check."},
]

app = FastAPI(
    title="Table Service",
    description="Manages restaurant tables — number, capacity and reservation status.",
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

app.include_router(table_router.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
