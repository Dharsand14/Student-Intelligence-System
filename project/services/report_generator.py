import pandas as pd
import numpy as np

def generate_report(data_list):
    """
    Generates a full report with data and summary statistics.
    Ensures consistent naming and robust calculation.
    """
    if not data_list:
        return pd.DataFrame(), {}
        
    df = pd.DataFrame(data_list)
    
    # Standardize Column Presence
    if 'predicted_score' not in df.columns:
        return df, {"Status": "Missing prediction column"}

    # Calculate Grade Counts
    def get_grade(s):
        if s >= 85: return 'A'
        if s >= 70: return 'B'
        if s >= 50: return 'C'
        return 'F'
    
    df['grade'] = df['predicted_score'].apply(get_grade)
    grade_counts = df['grade'].value_counts().to_dict()

    summary = {
        "total_records": len(df),
        "mean_score": round(df["predicted_score"].mean(), 2),
        "max_score": df["predicted_score"].max(),
        "min_score": df["predicted_score"].min(),
        "mean_study": round(df["study_hours"].mean(), 2) if 'study_hours' in df.columns else 0,
        "mean_att": round(df["attendance"].mean(), 2) if 'attendance' in df.columns else 0,
        "grades": grade_counts
    }

    return df, summary

def filter_data(df, student_id=None, threshold=None, above=True):
    """
    Generic filtering utility for reports.
    """
    temp_df = df.copy()
    if student_id:
        temp_df = temp_df[temp_df['student_id'] == student_id]
    
    if threshold is not None:
        if above:
            temp_df = temp_df[temp_df['predicted_score'] >= threshold]
        else:
            temp_df = temp_df[temp_df['predicted_score'] < threshold]
            
    return temp_df