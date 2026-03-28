import random
from database.users_db import add_user, add_student
from database.predictions_db import add_prediction

def generate_mock_data(num_students=10):
    """
    Populates local database with fake students and predictions for UI testing.
    """
    departments = ["CS", "IT", "AIML", "CTIS"]
    
    print(f"🌱 Seeding {num_students} mock users and their predictions...")
    
    for i in range(1, num_students + 1):
        email = f"testuser{i}@university.edu"
        student_id = f"STU{random.randint(1000, 9999)}"
        name = f"Demo Student {i}"
        
        try:
            add_user(username=email, password="password123", role="student")
            add_student(student_id=student_id, name=name, email=email)
            
            # Create a mock prediction for them
            mock_data = {
                "student_id": student_id,
                "study_hours": random.uniform(2, 9),
                "attendance": random.uniform(60, 100),
                "sleep_hours": random.uniform(4, 9),
                "mental_health": random.uniform(30, 90),
                "exam_scores": random.uniform(50, 95)
            }
            mock_predicted = min(100, (mock_data["study_hours"] * 3) + (mock_data["attendance"] * 0.5))
            
            add_prediction(mock_data, mock_predicted)
            print(f"  + Added {email} / {student_id}")
            
        except Exception as e:
            print(f"  - Skipped {email}: {e}")
            
    print("✅ Seeding complete!")

if __name__ == "__main__":
    generate_mock_data(10)
