from fastapi import FastAPI
from app.routes import user, role
from app.database import get_database

app = FastAPI(title="User Service", docs_url="/docs")


@app.on_event("startup")
def startup() -> None:
    db = get_database()
    db["users"].create_index("username", unique=True)
    db["users"].create_index("email", unique=True)
    db["roles"].create_index("name", unique=True)
    db["roles"].update_one(
        {"name": "customer"},
        {"$setOnInsert": {"description": "Default role for self-registered users"}},
        upsert=True,
    )

app.include_router(user.router)
app.include_router(role.router)

@app.get("/")
def root():
    return {"message": "User Service is running"}

# To run: uvicorn app.main:app --host 0.0.0.0 --port 8007
