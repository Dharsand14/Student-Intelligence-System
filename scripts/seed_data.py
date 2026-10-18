import random
import secrets

from database.predictions_db import add_prediction
from database.users_db import add_student, add_user


def generate_mock_data(num_students=10):
    """Populate the local database with mock users and predictions for UI testing."""
    print(f"Seeding {num_students} mock users and their predictions...")

    for i in range(1, num_students + 1):
        email = f"testuser{i}@university.edu"
        student_id = f"STU{random.randint(1000, 9999)}"
        name = f"Student {i}"

        try:
            add_user(
                username=email,
                password=secrets.token_urlsafe(32),
                role="student",
            )
            add_student(student_id=student_id, name=name, email=email)

            mock_data = {
                "student_id": student_id,
                "study_hours": random.uniform(2, 9),
                "attendance": random.uniform(60, 100),
                "mental_health": random.uniform(3, 9),
                "sleep_hours": random.uniform(5, 9),
                "exam_scores": random.uniform(40, 95),
            }
            mock_predicted = min(
                98,
                (mock_data["study_hours"] * 4) + (mock_data["attendance"] * 0.4),
            )

            add_prediction(mock_data, mock_predicted)
            print(f"  + Added: {email} / {student_id}")

        except Exception as e:
            print(f"  - Error for {email}: {e}")

    print("Seed complete successfully.")


if __name__ == "__main__":
    generate_mock_data(10)
