import sqlite3

def check_users():
    conn = sqlite3.connect('algora.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if not cursor.fetchone():
            print("Table 'users' does not exist.")
            return

        cursor.execute("SELECT id, username FROM users;")
        users = cursor.fetchall()
        if not users:
            print("No users found in the database.")
        else:
            print(f"Found {len(users)} users:")
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_users()
