import pandas as pd
import os
from datetime import datetime

FILE_PATH = "data/predictions.xlsx"


# -------------------------------
# 📁 INIT FILE
# -------------------------------
def init_file():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=[
            "student_id",
            "study_hours",
            "attendance",
            "sleep_hours",
            "mental_health",
            "exam_scores",
            "predicted_score",
            "created_at"
        ])
        df.to_excel(FILE_PATH, index=False)


# -------------------------------
# ➕ ADD PREDICTION
# -------------------------------
def add_prediction(data, prediction):
    init_file()

    df = pd.read_excel(FILE_PATH)

    new_row = {
        "student_id": data.get("student_id"),
        "study_hours": data.get("study_hours"),
        "attendance": data.get("attendance"),
        "sleep_hours": data.get("sleep_hours"),
        "mental_health": data.get("mental_health"),
        "exam_scores": data.get("exam_scores"),
        "predicted_score": float(prediction),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_excel(FILE_PATH, index=False)


# -------------------------------
# 📊 GET ALL
# -------------------------------
def get_all():
    init_file()
    return pd.read_excel(FILE_PATH)


# -------------------------------
# 👤 GET BY STUDENT
# -------------------------------
def get_by_student(student_id):
    df = get_all()
    return df[df["student_id"] == student_id]