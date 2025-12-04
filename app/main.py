from fastapi import FastAPI
from app.api.v1.endpoints import notes
from app.db.base import Base
from app.db.session import engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Notes")

app.include_router(notes.router, prefix="/notes", tags=["notes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Notes API"}
