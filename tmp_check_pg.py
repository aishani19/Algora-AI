import sqlalchemy
from sqlalchemy import create_engine, text

DATABASE_URL ="postgresql://postgres:newpassword123@localhost:5432/algora"

def check_db():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM users"))
            users = result.fetchall()
            if not users:
                print("No users in 'users' table.")
            else:
                print(f"Found {len(users)} users:")
                for user in users:
                    print(user)
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")

if __name__ == "__main__":
    check_db()
