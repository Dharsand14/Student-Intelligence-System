from database.db_sqlite import get_connection
from utils.security import hash_password


# -------------------------------
# ➕ ADD USER (SAFE + CLEAN)
# -------------------------------
def add_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 🔍 Check if user exists
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            raise ValueError("User already exists")

        # 🔐 Hash password
        hashed_password = hash_password(password)

        # ✅ Insert user
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )

        conn.commit()

    finally:
        conn.close()


# -------------------------------
# 🔍 GET USER
# -------------------------------
def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT username, password, role FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()

        if row:
            return {
                "username": row[0],
                "password": row[1],
                "role": row[2]
            }
        return None

    finally:
        conn.close()


# -------------------------------
# 📋 GET ALL USERS
# -------------------------------
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT username, role FROM users")
        users = cursor.fetchall()
        return users

    finally:
        conn.close()


# -------------------------------
# ❌ DELETE USER
# -------------------------------
def delete_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()

    finally:
        conn.close()