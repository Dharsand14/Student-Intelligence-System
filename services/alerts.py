def check_failing_students(predictions_df, threshold=40.0):
    """
    Scans a dataframe of predictions and returns a list of prioritized alerts
    for students whose predicted score is below the safe threshold.
    """
    alerts = []
    if predictions_df is None or predictions_df.empty:
        return alerts
        
    for _, row in predictions_df.iterrows():
        score = row.get("predicted_score", 100)
        student_id = row.get("student_id", "Unknown")
        
        # 🚨 Emergency Risk (Immediate staff intervention)
        if score < 20:
             alerts.append({
                "level": "Emergency",
                "student_id": student_id,
                "score": score,
                "message": f"CRITICAL: Student {student_id} is at extreme risk ({score:.2f}%). Immediate support required."
            })
        # ⚠️ High Risk (Mentor follow-up)
        elif score < threshold:
            alerts.append({
                "level": "Warning",
                "student_id": student_id,
                "score": score,
                "message": f"Warning: Student {student_id} is falling behind ({score:.2f}%)."
            })
            
    # Sort alerts by severity (Emergency first)
    alerts.sort(key=lambda x: 0 if x["level"] == "Emergency" else 1)
    
    return alerts
