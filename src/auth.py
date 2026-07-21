import bcrypt

# from src.database import get_connection
from database import get_connection

def hash_password(password):
    """Hash a plain text password using bcrypt."""
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password.decode("utf-8")


def verify_password(password, hashed_password):
    """Verify a plain text password against a hashed password."""
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_bytes)


def register_user(username, password):
    """Register a new user in the database."""

    conn = get_connection()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    if cursor.fetchone():
        conn.close()
        return False, "Username already exists."

    # Hash the password
    hashed_password = hash_password(password)

    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )

    conn.commit()
    conn.close()

    return True, "User registered successfully."

def login_user(username, password):
    """Authenticate a user."""

    conn = get_connection()
    cursor = conn.cursor()

    # Find user by username
    cursor.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    # Check if user exists
    if user is None:
        return False, "User does not exist."

    user_id, username, hashed_password = user

    # Verify password
    if verify_password(password, hashed_password):
        return True, {
            "id": user_id,
            "username": username
        }

    return False, "Incorrect password."

# if __name__ == "__main__":
#     # Register user
#     success, message = register_user("akshat", "MyPassword123")
#     print("Register:", success, "-", message)

#     # Login with correct password
#     success, data = login_user("akshat", "MyPassword123")
#     print("Login (Correct):", success, "-", data)

#     # Login with wrong password
#     success, data = login_user("akshat", "WrongPassword")
#     print("Login (Wrong):", success, "-", data)