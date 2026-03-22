from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import delivery as delivery_router
from app.config import settings
from app.database import init_db
from app.models.delivery import Delivery


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Delivery])
    yield


tags_metadata = [
    {"name": "deliveries", "description": "Track deliveries — driver assignment and status from pickup to delivered."},
    {"name": "health",     "description": "Service health check."},
]

app = FastAPI(
    title="Delivery Service",
    description="Tracks order deliveries — driver, address, and status lifecycle.",
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

app.include_router(delivery_router.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
