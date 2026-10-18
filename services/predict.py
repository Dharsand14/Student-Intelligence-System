import joblib
import numpy as np
import os

# Global model cache
model = None


# -------------------------------
# 🔄 LOAD MODEL (SAFE + CACHED)
# -------------------------------
def load_model():
    global model

    if model is None:
        model_path = os.path.join("models", "best_model.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"❌ Model file not found at: {model_path}"
            )

        try:
            model = joblib.load(model_path)
            print("Model loaded successfully")

        except Exception as e:
            raise RuntimeError(f"Error loading model: {e}")

    return model


# -------------------------------
# 🎯 PREDICTION FUNCTION
# -------------------------------
def predict(data):
    try:
        mdl = load_model()

        # Input Scaling: If hours > 24, assume weekly input and divide by 7
        study_val = float(data.get("study_hours", 0))
        if study_val > 24:
            study_val = round(study_val / 7, 2)
            data["scaled_daily"] = True
        else:
            data["scaled_daily"] = False

        # ✅ New Feature Order from Imported Project:
        # [study_hours, attendance, mental_health, sleep_hours, exam_scores]
        features = np.array([[
            study_val,
            float(data.get("attendance", 0)),
            float(data.get("mental_health", 0)),
            float(data.get("sleep_hours", 0)),
            float(data.get("exam_scores", 0))
        ]])

        prediction = mdl.predict(features)
        result = float(prediction[0])
        result = max(0, min(result, 100))

        # Classification + Styling Logic
        if result >= 85:
            grade, grade_class, grade_icon, score_color = "A — Excellent", "grade-A", "🏆", "#6ee7b7"
        elif result >= 70:
            grade, grade_class, grade_icon, score_color = "B — Good", "grade-B", "✅", "#6ee7b7"
        elif result >= 50:
            grade, grade_class, grade_icon, score_color = "C — Average", "grade-C", "⚠️", "#fcd34d"
        else:
            grade, grade_class, grade_icon, score_color = "F — At Risk", "grade-F", "🚨", "#fca5a5"

        # 📝 AUDIT LOG
        try:
            from utils.logger import log_event
            log_event("PREDICTION_MADE", data.get("student_id", "Anonymous"), {
                "score": round(result, 2),
                "study": study_val,
                "attendance": data.get("attendance", 0),
                "was_weekly": data.get("scaled_daily", False)
            })
        except Exception:
            pass

        # Output Transformation: Return rich dictionary with UI metadata
        return {
            "score": round(result, 2),
            "original_input": data,
            "was_weekly": data.get("scaled_daily", False),
            "ui_metadata": {
                "grade": grade,
                "grade_class": grade_class,
                "grade_icon": grade_icon,
                "score_color": score_color
            }
        }

    except Exception as e:
        raise RuntimeError(f"❌ Prediction error: {e}")