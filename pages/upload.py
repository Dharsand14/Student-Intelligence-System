import pandas as pd
import streamlit as st
import time
from database.predictions_db import add_prediction
from services.predict import predict
from utils.file_handler import validate_prediction_df, convert_df_to_csv

def upload_page():
    st.title("📂 Bulk Prediction Ingestion")
    st.markdown("Rapidly process large cohorts of students using CSV or Excel datasets.")
    
    st.info("""
    📋 **Required Data Schema:**
    Ensure your file contains these headers: `student_id`, `study_hours`, `attendance`, `sleep_hours`, `mental_health`, `exam_scores`
    """)

    uploaded_file = st.file_uploader("Drop your dataset here", type=["csv", "xlsx"])

    if not uploaded_file:
        st.write("---")
        st.caption("Awaiting file upload... System will automatically clean and deduplicate your data.")
        return

    try:
        # Load Data
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # 🧼 VALIDATE & CLEAN (Using central utility)
        is_valid, err_msg = validate_prediction_df(df)
        
        if not is_valid:
            st.error(f"❌ Schema Validation Failed: {err_msg}")
            return

        st.success(f"📦 Successfully loaded and cleaned {len(df)} unique student records.")
        with st.expander("🔍 Preview Processed Data (First 5 Rows)"):
            st.dataframe(df.head(), use_container_width=True)

        if st.button("🚀 Execute Phase: Bulk Prediction", use_container_width=True, type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            processed_results = []
            
            # Start timer
            start_time = time.time()

            for idx, row in df.iterrows():
                try:
                    data_payload = {
                        "student_id": str(row["student_id"]),
                        "study_hours": float(row["study_hours"]),
                        "attendance": float(row["attendance"]),
                        "sleep_hours": float(row["sleep_hours"]),
                        "mental_health": float(row["mental_health"]),
                        "exam_scores": float(row["exam_scores"]),
                    }

                    # Prediction Integration
                    pred_resp = predict(data_payload)
                    score = pred_resp["score"]
                    
                    processed_results.append({**data_payload, "predicted_score": round(score, 2)})
                except Exception as e:
                    st.warning(f"Skipped Student {row.get('student_id', 'Unknown')}: {e}")

                # Update UI
                progress = (idx + 1) / len(df)
                progress_bar.progress(progress)
                status_text.text(f"Analyzing Record {idx + 1} of {len(df)}...")

            # 🚀 BATCH PERSISTENCE (Centralized Transaction)
            from database.predictions_db import add_predictions_batch
            add_predictions_batch(processed_results)

            duration = time.time() - start_time
            progress_bar.progress(1.0)
            status_text.text(f"Batch Processing Complete in {duration:.2f}s")

            st.balloons()
            st.success(f"✅ Successfully analyzed {len(processed_results)} students. Records persisted to database.")

            # Result Display & Export
            res_df = pd.DataFrame(processed_results)
            st.subheader("📊 Execution Results")
            st.dataframe(res_df, use_container_width=True)

            # Export
            csv_out = convert_df_to_csv(res_df)
            st.download_button(
                label="⬇️ Download Processed Intelligence CSV",
                data=csv_out,
                file_name=f"bulk_results_{int(time.time())}.csv",
                mime="text/csv",
                use_container_width=True
            )

    except Exception as e:
        st.error(f"❌ Critical Failure: {e}")
