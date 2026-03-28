import pandas as pd


# ✅ Generate full report (Data + Summary)
def generate_report(data):
    df = pd.DataFrame(data)

    if df.empty:
        return df, {}

    # 📊 Summary calculations
    summary = {
        "Total Records": len(df),
        "Average Score": round(df["predicted_score"].mean(), 2),
        "Highest Score": df["predicted_score"].max(),
        "Lowest Score": df["predicted_score"].min(),
        "Average Study Hours": round(df["study_hours"].mean(), 2),
        "Average Attendance": round(df["attendance"].mean(), 2)
    }

    return df, summary


# ✅ Convert to CSV (for download)
def export_csv(df):
    return df.to_csv(index=False).encode("utf-8")


# ✅ Filter by student
def filter_by_student(df, student_id):
    if "student_id" not in df.columns:
        return df
    return df[df["student_id"] == student_id]


# ✅ Filter low performers
def get_low_performers(df, threshold=40):
    return df[df["predicted_score"] < threshold]


# ✅ Top performers
def get_top_performers(df, threshold=80):
    return df[df["predicted_score"] >= threshold]