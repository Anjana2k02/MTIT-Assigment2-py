from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import location as location_router
from app.routes import table_status as table_status_router
from app.routes import table as table_router
from app.config import settings
from app.database import init_db
from app.models.location import Location
from app.models.table_status import TableStatus
from app.models.table import Table


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Location, TableStatus, Table])
    yield


tags_metadata = [
    {"name": "locations",      "description": "Manage restaurant locations/sections."},
    {"name": "table-statuses", "description": "Manage table status definitions (available, reserved, not-cleaned)."},
    {"name": "tables",         "description": "Manage restaurant tables linked to locations with status."},
    {"name": "health",         "description": "Service health check."},
]

app = FastAPI(
    title="Table Service",
    description="Manages restaurant locations, table statuses and tables.",
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

app.include_router(location_router.router,          prefix="/api/v1")
app.include_router(table_status_router.router,      prefix="/api/v1")
app.include_router(table_router.router,             prefix="/api/v1")
app.include_router(table_router.locations_router,   prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
