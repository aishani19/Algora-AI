from fastapi import FastAPI
# Triggers reload to recreate missing DB tables and load new auth modules
from backend.database import Base, engine
from backend import models   

from backend.routes import roadmap, analyzer, dashboard, auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(roadmap.router, prefix="/roadmap")
app.include_router(analyzer.router, prefix="/analyze")
app.include_router(dashboard.router, prefix="/dashboard")

@app.get("/")
def root():
    return {"message": "Algora AI running"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

from sqlalchemy.orm import Session
from fastapi import Depends
from backend.database import get_db

@app.get("/ping_db")
def ping_db(db: Session = Depends(get_db)):
    return {"status": "db_ok"}