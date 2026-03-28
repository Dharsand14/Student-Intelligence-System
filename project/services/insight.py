def generate_class_insights(df):
    """
    Generates human-readable text insights from an entire class dataframe.
    """
    insights = []
    if df is None or df.empty:
        return ["No data available to generate insights."]
        
    avg_score = df['predicted_score'].mean()
    insights.append(f"🎓 **Class Average:** The predicted class average is **{avg_score:.2f}%**.")
    
    low_attendance = df[df['attendance'] < 75]
    if not low_attendance.empty:
        insights.append(f"⚠️ **Attendance Warning:** {len(low_attendance)} students have attendance below 75%.")
        
    high_performers = df[df['predicted_score'] >= 85]
    if not high_performers.empty:
        insights.append(f"⭐ **Top Performers:** {len(high_performers)} students are predicted to score an A grade (85%+).")
        
    return insights
