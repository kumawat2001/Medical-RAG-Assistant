import sqlite3
from pathlib import Path

# Create the database directory if it doesn't exist
DB_DIR = Path("database")
DB_DIR.mkdir(parents=True, exist_ok=True)

# Database file path
DB_PATH = DB_DIR / "users.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def create_users_table():
    """Create the users table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_users_table()
    print("Users table created successfully!")