import sys
import os
import pytest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.predict import predict
from services.recommendation import get_study_recommendations
from services.alerts import check_failing_students

def test_integration_prediction_and_recommendation():
    # Simulate a high-risk student
    data = {
        "student_id": "S_INT_01",
        "study_hours": 1.0,  # low
        "attendance": 45.0,  # low
        "mental_health": 3.0, # low
        "sleep_hours": 5.0,
        "exam_scores": 30.0   # low
    }
    # 1. Prediction
    pred = predict(data)
    score = pred["score"]
    
    # 2. Recommendation based on features
    recs = get_study_recommendations(
        study_hours=data["study_hours"],
        attendance=data["attendance"],
        sleep_hours=data["sleep_hours"],
        predicted_score=score
    )
    
    # Assertions
    assert score < 60  # Should be low
    assert len(recs) >= 1
    # Check if ANY string in recs contains 'attendance' or 'study' (case insensitive)
    assert any("attendance" in r.lower() for r in recs) or any("study" in r.lower() for r in recs)

def test_alerts_logic():
    # Large dataset with a failing student
    mock_df = [
        {"student_id": "S1", "predicted_score": 90.0},
        {"student_id": "S2", "predicted_score": 15.0},  # Failing
        {"student_id": "S3", "predicted_score": 65.0}
    ]
    import pandas as pd
    df = pd.DataFrame(mock_df)
    
    alerts = check_failing_students(df)
    
    # Verify S2 triggered an alert
    assert any("S2" in a["message"] for a in alerts)
    assert len(alerts) >= 1

if __name__ == "__main__":
    test_integration_prediction_and_recommendation()
    test_alerts_logic()
    print("Integration / API layer tests passed!")
