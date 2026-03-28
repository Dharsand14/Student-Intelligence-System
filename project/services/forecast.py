import pandas as pd
import numpy as np

def forecast_next_score(student_history_df):
    """
    Analyzes a student's past predictions to forecast their trajectory.
    Returns a dictionary with trend string and expected next score.
    """
    if student_history_df is None or len(student_history_df) < 2:
        return {"trend": "Not enough data", "next_expected": None}
    
    # Sort chronological
    df = student_history_df.sort_values(by="created_at")
    scores = df["predicted_score"].tolist()
    
    # Calculate simple moving average trend
    recent_diff = scores[-1] - scores[0]
    
    if recent_diff > 2:
        trend = "Improving 📈"
    elif recent_diff < -2:
        trend = "Declining 📉"
    else:
        trend = "Stable ➡️"
        
    # Simple linear extrapolation for next score
    avg_change = np.mean(np.diff(scores))
    next_score = min(100, max(0, scores[-1] + avg_change))
    
    return {
        "trend": trend,
        "next_expected": round(next_score, 2)
    }
