from backend.database import engine
from sqlalchemy import text

def drop_tables():
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS roadmaps CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS analyses CASCADE;"))
        conn.commit()
    print("Tables dropped successfully.")

if __name__ == "__main__":
    drop_tables()
