import sys
import os
import pytest
import numpy as np
import joblib
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.predict import predict
from scripts.retrain_model import train_model


def test_training_supports_excel_exam_scores_and_four_inputs(tmp_path):
    dataset = pd.DataFrame({
        "study_hours": np.linspace(1, 6, 24),
        "attendance": np.linspace(55, 100, 24),
        "sleep_hours": np.linspace(5, 9, 24),
        "mental_health": np.linspace(2, 10, 24),
        "exam_scores": np.linspace(40, 95, 24),
    })
    dataset_path = tmp_path / "student_data.xlsx"
    model_path = tmp_path / "best_model.pkl"
    dataset.to_excel(dataset_path, index=False)

    metrics = train_model(str(dataset_path), str(model_path))
    estimator = joblib.load(model_path)

    assert metrics["rows"] == len(dataset)
    assert list(estimator.feature_names_in_) == [
        "study_hours",
        "attendance",
        "mental_health",
        "sleep_hours",
    ]

def test_predict_standard_input():
    # Test case with common daily values
    data = {
        "study_hours": 3.5,
        "attendance": 85.0,
        "mental_health": 8.0,
        "sleep_hours": 7.0,
    }
    
    result = predict(data)
    
    # Assert result is a float (or dictionary if your latest version returns rich data)
    # Checking our latest predict.py: it returns a DICTIONARY with 'score', 'grade', etc.
    assert isinstance(result, dict)
    assert "score" in result
    assert "grade" in result["ui_metadata"]
    assert 0 <= result["score"] <= 120 # LinearRegression can overshoot but we expect logical ranges

def test_predict_weekly_scaling():
    # Test if 35 study hours (weekly) is scaled down automatically (35 / 7 = 5)
    data = {
        "study_hours": 35.0, # clearly weekly
        "attendance": 90.0,
        "mental_health": 9.0,
        "sleep_hours": 8.0,
    }
    
    result = predict(data)
    assert result["was_weekly"] is True
    assert result["score"] == 50.0

def test_predict_edge_cases():
    # Test with 0 or low values
    data = {
        "study_hours": 0,
        "attendance": 0,
        "mental_health": 1,
        "sleep_hours": 4,
    }
    result = predict(data)
    assert result["score"] < 100 # Should be lower than a high-performer

if __name__ == "__main__":
    # If run directly
    test_predict_standard_input()
    test_predict_weekly_scaling()
    test_predict_edge_cases()
    print("All model tests passed!")
