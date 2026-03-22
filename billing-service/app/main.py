from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import billing as billing_router
from app.config import settings
from app.database import init_db
from app.models.billing import Invoice


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Invoice])
    yield


tags_metadata = [
    {"name": "billing", "description": "Generate and manage invoices — subtotal, tax, total, payment status."},
    {"name": "health",  "description": "Service health check."},
]

app = FastAPI(
    title="Billing Service",
    description="Handles invoice generation and payment tracking for customer orders.",
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

app.include_router(billing_router.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
