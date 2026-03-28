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
            print("✅ Model loaded successfully")

        except Exception as e:
            raise RuntimeError(f"❌ Error loading model: {e}")

    return model


# -------------------------------
# 🎯 PREDICTION FUNCTION
# -------------------------------
def predict(data):
    try:
        mdl = load_model()

        # ✅ Validate required fields
        required_fields = [
            "study_hours",
            "attendance",
            "sleep_hours",
            "mental_health",
            "exam_scores"
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"❌ Missing field: {field}")

        # ✅ Convert safely to float
        features = np.array([[
            float(data["study_hours"]),
            float(data["attendance"]),
            float(data["sleep_hours"]),
            float(data["mental_health"]),
            float(data["exam_scores"])
        ]])

        # ✅ Predict
        prediction = mdl.predict(features)

        # ✅ Ensure valid output
        if prediction is None or len(prediction) == 0:
            raise ValueError("❌ Model returned empty prediction")

        result = float(prediction[0])

        # Optional: clamp value (0–100)
        result = max(0, min(result, 100))

        return result

    except Exception as e:
        raise RuntimeError(f"❌ Prediction error: {e}")