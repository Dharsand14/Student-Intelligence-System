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

    # ✅ Generate advanced report
    st.subheader("📑 Generate Full Report")

    if st.button("Generate Summary Text Report"):
        try:
            # ✅ PASS DATA TO FUNCTION
            df_report, summary = generate_report(data)
            
            # Format report as text
            report_text = "📊 FULL STUDENT SUMMARY REPORT 📊\n"
            report_text += "=" * 35 + "\n\n"
            for k, v in summary.items():
                report_text += f"✔️ {k}: {v}\n"

            st.success("Report generated successfully!")

            st.download_button(
                label="Download Summary Report",
                data=report_text.encode("utf-8"),
                file_name="summary_report.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error generating report: {e}")