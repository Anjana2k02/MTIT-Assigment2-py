from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import store as store_router
from app.config import settings
from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


tags_metadata = [
    {"name": "store",  "description": "Track inventory items — quantity, unit and low-stock threshold."},
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


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
