import sys
import os
import pytest
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.explainability import explain_prediction
from services.insight import generate_class_insights
from services.forecast import forecast_next_score

def test_explain_prediction():
    data = {
        "study_hours": 2.0,  # Low
        "attendance": 98.0, # High
        "sleep_hours": 5.0,  # Low
        "mental_health": 9.0 # High
    }
    explanation = explain_prediction(data)
    assert "+ Perfect attendance" in explanation
    assert "- Low study hours" in explanation
    assert "- Inadequate sleep" in explanation

def test_generate_class_insights():
    df = pd.DataFrame([
        {"student_id": "S1", "predicted_score": 90.0, "attendance": 100, "sleep_hours": 8, "study_hours": 7},
        {"student_id": "S2", "predicted_score": 90.0, "attendance": 100, "sleep_hours": 8, "study_hours": 7},
        {"student_id": "S3", "predicted_score": 20.0, "attendance": 40, "sleep_hours": 4, "study_hours": 1} # Combined risk
    ])
    insights = generate_class_insights(df)
    assert any("Class Average" in i for i in insights)
    assert any("Critical Risk Pattern" in i for i in insights) # S3 triggered it
    assert any("Strong Prep" in i for i in insights) # S1, S2 triggered it

def test_forecast_next_score():
    # Historical data for a student
    history = pd.DataFrame([
        {"created_at": "2024-03-01 10:00:00", "predicted_score": 50.0},
        {"created_at": "2024-03-05 10:00:00", "predicted_score": 55.0},
        {"created_at": "2024-03-10 10:00:00", "predicted_score": 60.0}
    ])
    forecast = forecast_next_score(history)
    assert "Improving" in forecast["trend"]
    assert forecast["next_expected"] > 60.0
    assert "confidence" in forecast
    assert forecast["avg_growth_rate"] == 5.0

if __name__ == "__main__":
    test_explain_prediction()
    test_generate_class_insights()
    test_forecast_next_score()
    print("Service enhancements tests passed!")
