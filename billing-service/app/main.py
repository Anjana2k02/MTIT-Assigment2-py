from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import billing as pos_router
from app.routes import discount as discount_router
from app.routes import bill as bill_router
from app.config import settings
from app.database import init_db
from app.models.billing import PosOrder
from app.models.discount import Discount


async def _seed_discounts():
    if await Discount.count() == 0:
        defaults = [
            Discount(name="no-discount", amount=0.0),
            Discount(name="corporate",   amount=10.0),
            Discount(name="new-year",    amount=7.0),
            Discount(name="christmas",   amount=12.0),
        ]
        for d in defaults:
            await d.insert()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([PosOrder, Discount])
    await _seed_discounts()
    yield


tags_metadata = [
    {"name": "pos",      "description": "Create and manage POS orders — item list, totals, discount, tax, and payment status. Supports dining and delivery order types."},
    {"name": "discount", "description": "Manage discounts — name and percentage amount applied to POS orders."},
    {"name": "bill",     "description": "Generate a full bill breakdown for a POS order — subtotal, discount, tax, and total."},
    {"name": "health",   "description": "Service health check."},
]

app = FastAPI(
    title="Billing Service",
    description="POS billing service — manages orders, applies discounts, computes totals, and generates itemised bills.",
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

app.include_router(pos_router.router,      prefix="/api/v1")
app.include_router(discount_router.router, prefix="/api/v1")
app.include_router(bill_router.router,     prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
