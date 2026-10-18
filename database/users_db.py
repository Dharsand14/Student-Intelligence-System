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
# 🎓 ADD STUDENT
# -------------------------------
def add_student(student_id, name, email):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO students (student_id, name, email) VALUES (?, ?, ?)",
            (student_id, name, email)
        )
        conn.commit()
    except Exception as e:
        print(f"Error adding student: {e}")
        raise e
    finally:
        conn.close()


# -------------------------------
# 🎓 GET STUDENT BY EMAIL
# -------------------------------
def get_student_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT student_id, name, email FROM students WHERE email = ?", (email,))
        row = cursor.fetchone()

        if row:
            return {
                "student_id": row[0],
                "name": row[1],
                "email": row[2]
            }
        return None
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


# -------------------------------
# 📦 BATCH OPERATIONS (NEW)
# -------------------------------
def add_students_batch(students_list):
    """
    Automates the mass registration of student profiles.
    Used during high-capacity CSV/Excel cohort imports.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        data = [
            (s.get("student_id"), s.get("name"), s.get("email"))
            for s in students_list
        ]
        cursor.executemany(
            "INSERT INTO students (student_id, name, email) VALUES (?, ?, ?)",
            data
        )
        conn.commit()
    except Exception as e:
        print(f"Error in student batch insert: {e}")
    finally:
        conn.close()