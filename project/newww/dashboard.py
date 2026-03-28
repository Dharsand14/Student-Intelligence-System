import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from database.db_excel import delete_last_record, clear_database

def show_dashboard():

    st.title("📊 Student Performance Dashboard")

    DB_FILE = "student_database.xlsx"

    if st.button("🔄 Refresh Dashboard"):
        st.rerun()

    if os.path.exists(DB_FILE):

        df = pd.read_excel(DB_FILE)

        # ⭐ Ensure Date Time column exists and keep it last
        if "Date Time" not in df.columns:
            df["Date Time"] = ""

        if df.empty:
            st.warning("⚠️ No predictions stored yet")
            return
        
        # ⭐ Show Student ID first and Attendance second
        if "Student ID" in df.columns and "Attendance" in df.columns:
            cols = ["Student ID", "Attendance"] + [
                col for col in df.columns if col not in ["Student ID", "Attendance"]
            ]
            df = df[cols]

        # ⭐ Summary Metrics
        col1, col2 = st.columns(2)

        with col1:
            st.metric("👥 Total Predictions", len(df))

        with col2:
            avg_perf = df["Predicted Performance"].mean()
            st.metric("📈 Average Performance", f"{avg_perf:.2f}%")

        st.divider()

        # ⭐ Show Table
        st.subheader("📁 Prediction History")
        st.dataframe(df, use_container_width=True)

        st.divider()

        # ⭐ Controls
        col1, col2 = st.columns(2)

        with col1:
            if st.button("❌ Delete Last Prediction"):
                if delete_last_record():
                    st.success("Last record deleted 🗑️")
                    st.rerun()

        with col2:
            if st.button("🗑️ Clear Database"):
                if clear_database():
                    st.success("Database cleared 💥")
                    st.rerun()

        st.divider()

        # ⭐ Download
        with open(DB_FILE, "rb") as f:
            st.download_button("⬇️ Download Database", f, file_name=DB_FILE)

        # ⭐ Charts
        st.subheader("📈 Performance Analytics")

        # Line chart
        st.write("Performance Trend")
        st.line_chart(df["Predicted Performance"])

        # Bar chart
        if "Study Hours" in df.columns:
            st.write("Study Hours vs Performance")
            st.bar_chart(df[["Study Hours", "Predicted Performance"]])

        # ⭐ Pie chart for performance levels
        st.subheader("🥧 Performance Distribution")

        def categorize(score):
            if score < 40:
                return "Low"
            elif score < 70:
                return "Average"
            else:
                return "Good"

        df["Category"] = df["Predicted Performance"].apply(categorize)

        category_counts = df["Category"].value_counts()

        fig, ax = plt.subplots()
        ax.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%")
        ax.set_title("Student Performance Levels")

        st.pyplot(fig)

        st.divider()

    else:
        st.warning("⚠️ No database found. Please make predictions first.")