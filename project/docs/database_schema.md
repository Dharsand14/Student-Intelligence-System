# 🗄️ Database Schema & Record Persistence

The Student Performance System uses a structured **SQLite** database (`students.db`) for all storage requirements.

---

## 👥 Table: `users`
Manages the authentication and role-based access control (RBAC) of the application.
- `id` (INT - Primary Key)
- `username` (TEXT - Unique, email-based)
- `password` (TEXT - Hashed with `bcrypt`)
- `role` (TEXT - `student` or `staff`)
- `created_at` (DATETIME)

## 👨‍🎓 Table: `students`
Stores the academic profile of the student and correlates with their user account.
- `id` (INT - Primary Key)
- `student_id` (TEXT - Unique Identifier)
- `name` (TEXT)
- `email` (TEXT - Foreign Key to `users.username`)
- `created_at` (DATETIME)

## 📈 Table: `predictions`
Captures every AI-driven inference made for tracking and trend analysis.
- `id` (INT - Primary Key)
- `student_id` (TEXT - Foreign Key to `students.student_id`)
- `study_hours` (FLOAT)
- `attendance` (FLOAT)
- `sleep_hours` (FLOAT)
- `mental_health` (FLOAT)
- `exam_scores` (FLOAT)
- `predicted_score` (FLOAT - Result from AI model)
- `created_at` (DATETIME)

## 💬 Table: `feedback`
Stores student-provided ratings and comments for administrative review.
- `id` (INT - Primary Key)
- `username` (TEXT)
- `feedback_text` (TEXT - XSS Sanitized)
- `rating` (INT - 1-5 scale)
- `timestamp` (DATETIME)

---
*Database Version: 2.2.0 | Last Modified: 2026-03-29*
