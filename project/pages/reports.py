import streamlit as st
import pandas as pd
from database.predictions_db import get_all_predictions
from services.report_generator import generate_report, export_csv


def reports_page():
    st.title("📄 Reports & Predictions History")

    # ✅ Load prediction data
    data = get_all_predictions()

    if not data:
        st.warning("No prediction data available")
        return

    # Convert to DataFrame
    df = pd.DataFrame(data)

    st.subheader("📊 Prediction History")
    st.dataframe(df)

    # ✅ Filters (optional but useful)
    st.subheader("🔍 Filter Data")

    if "student_id" in df.columns:
        student_filter = st.text_input("Filter by Student ID")

        if student_filter:
            df = df[df["student_id"].astype(str).str.contains(student_filter)]
            st.dataframe(df)

    # ✅ Download as CSV
    st.subheader("⬇️ Download Report")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="student_predictions.csv",
        mime="text/csv"
    )

    # ✅ Generate advanced report (PDF/CSV from service)
    st.subheader("📑 Generate Full Report")

    if st.button("Generate Report"):
        try:
            file = generate_report()

            st.success("Report generated successfully!")

            st.download_button(
                label="Download Full Report",
                data=file,
                file_name="full_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Error generating report: {e}")