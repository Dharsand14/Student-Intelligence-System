import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# 📂 Load dataset (Excel + CSV fallback)
def load_data():
    excel_path = "data/student_database.xlsx"
    csv_path = "data/student_database.csv"

    if os.path.exists(excel_path):
        try:
            df = pd.read_excel(excel_path, engine="openpyxl")
            print("✅ Loaded Excel file")
            return df
        except Exception as e:
            print("⚠️ Excel load failed:", e)

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print("✅ Loaded CSV file")
        return df

    raise FileNotFoundError("❌ Dataset not found in data/ folder")


def train_model():
    df = load_data()

    print("📊 Dataset Loaded Successfully!")
    print("Columns:", df.columns.tolist())

    # ✅ Required columns
    required_columns = [
        "study_hours",
        "attendance",
        "sleep_hours",
        "mental_health",
        "exam_scores",
        "final_score"
    ]

    # 🔍 Check columns
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"❌ Missing column: {col}")

    # 🎯 Features
    X = df[
        [
            "study_hours",
            "attendance",
            "sleep_hours",
            "mental_health",
            "exam_scores",
        ]
    ]

    y = df["final_score"]

    # ✂️ Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 🤖 Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 📊 Evaluation
    preds = model.predict(X_test)
    error = mean_absolute_error(y_test, preds)

    print(f"📉 Model MAE: {error:.2f}")

    # 💾 Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/best_model.pkl")

    print("✅ Model saved successfully at models/best_model.pkl")


if __name__ == "__main__":
    train_model()