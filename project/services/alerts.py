def check_failing_students(predictions_df, threshold=40.0):
    """
    Scans a dataframe of predictions and returns a list of alerts
    for students whose predicted score is below the safe threshold.
    """
    alerts = []
    if predictions_df is None or predictions_df.empty:
        return alerts
        
    for _, row in predictions_df.iterrows():
        score = row.get("predicted_score", 100)
        if score < threshold:
            student_id = row.get("student_id", "Unknown")
            alerts.append({
                "level": "critical",
                "message": f"Student {student_id} is at risk with a predicted score of {score:.2f}%."
            })
    return alerts
