import pandas as pd
import numpy as np

def forecast_next_score(student_history_df):
    """
    Analyzes a student's past predictions to forecast their future trajectory.
    Adds confidence levels and growth rates.
    """
    if student_history_df is None or len(student_history_df) < 2:
        return {
            "trend": "Stable (Base)", 
            "next_expected": None, 
            "confidence": "Low",
            "message": "More data points needed for accurate trajectory."
        }
    
    # Sort chronological by created_at
    df = student_history_df.copy()
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.sort_values(by="created_at")
    
    scores = df["predicted_score"].tolist()
    
    # 📈 TREND CALCULATION (Last 3 points vs first)
    recent_diff = scores[-1] - scores[0]
    
    if recent_diff > 3:
        trend = "Improving"
        status_icon = "growth"
    elif recent_diff < -3:
        trend = "Declining"
        status_icon = "risk"
    else:
        trend = "Stable"
        status_icon = "steady"
        
    # 📊 LINEAR EXTRAPOLATION
    # Calculate average change between points
    changes = np.diff(scores)
    avg_change = np.mean(changes)
    
    # Check consistency (standard deviation of changes)
    # If changes are wildly different, confidence is low.
    if len(changes) > 1:
        volatility = np.std(changes)
        confidence = "High" if volatility < 5 else "Medium"
    else:
        confidence = "Medium"

    next_score = min(100, max(0, scores[-1] + avg_change))
    
    return {
        "trend": trend,
        "status_icon": status_icon,
        "next_expected": round(next_score, 2),
        "avg_growth_rate": round(avg_change, 2),
        "confidence": confidence,
        "points_analyzed": len(scores)
    }
