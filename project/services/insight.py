import pandas as pd

def generate_class_insights(df):
    """
    Generates intelligent human-readable insights from an entire class dataframe.
    """
    insights = []
    if df is None or df.empty:
        return ["No data available to generate insights."]
        
    avg_score = df['predicted_score'].mean()
    insights.append(f"Class Average: The predicted class average is {avg_score:.2f}%.")
    
    # Check Attendance Correlation
    low_attendance = df[df['attendance'] < 75]
    if not low_attendance.empty:
        insights.append(f"Attendance Risk: {len(low_attendance)} students have attendance below 75%. They average {low_attendance['predicted_score'].mean():.2f}% vs Class Average.")
        
    # High Performers
    high_performers = df[df['predicted_score'] >= 85]
    if not high_performers.empty:
        insights.append(f"Top Performers: {len(high_performers)} students are on track for an A grade (85%+).")
        
    # NEW: Risk Factor Analysis (Combined indicators)
    critical_risk = df[(df['attendance'] < 60) & (df['sleep_hours'] < 6)]
    if not critical_risk.empty:
        insights.append(f"Critical Risk Pattern: {len(critical_risk)} students show combined low attendance and poor sleep. Priority intervention required.")
        
    # NEW: Positive Behavior Recognition
    solid_prep = df[(df['study_hours'] >= 6) & (df['attendance'] >= 90)]
    if not solid_prep.empty:
        insights.append(f"Strong Prep: {len(solid_prep)} students have perfect attendance and high study hours.")
            
    return insights
