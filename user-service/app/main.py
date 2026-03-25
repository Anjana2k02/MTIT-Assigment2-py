from fastapi import FastAPI
from app.routes import user, role
from app.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service", docs_url="/docs")

app.include_router(user.router)
app.include_router(role.router)

@app.get("/")
def root():
    return {"message": "User Service is running"}

# To run: uvicorn app.main:app --host 0.0.0.0 --port 8007
