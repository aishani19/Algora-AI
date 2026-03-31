import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------ DATABASE CONFIG ------------------
try:
    DATABASE_URL = st.secrets["DATABASE_URL"]
except:
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Use fallback only for local development, otherwise allow it to fail clearly later
    DATABASE_URL = "postgresql://postgres:newpassword123@localhost:5432/algora"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()