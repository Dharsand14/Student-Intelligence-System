import streamlit as st
import pandas as pd
from services.monitoring import get_system_metrics
from database.users_db import get_all_users
from database.audit_db import get_audit_trail
from scripts.backup_db import backup_database
from scripts.retrain_model import retrain_random_forest
from database.predictions_db import get_all_predictions
from services.alerts import check_failing_students

def admin_panel():
    st.title("👨‍💼 Administrator Panel")
    
    tab1, tab2, tab3, tab4 = st.tabs(["System Metrics", "User Management", "Audit Logs", "System Controls"])
    
    with tab1:
        st.subheader("System Health")
        metrics = get_system_metrics()
        col1, col2, col3 = st.columns(3)
        col1.metric("CPU Usage", f"{metrics['cpu']}%")
        col2.metric("Memory Usage", f"{metrics['memory']}%")
        col3.metric("Disk Usage", f"{metrics['disk']}%")
        
        st.markdown("---")
        st.subheader("⚠️ Critical Student Alerts")
        all_preds = get_all_predictions()
        if all_preds:
            df_preds = pd.DataFrame(all_preds)
            alerts = check_failing_students(df_preds)
            if alerts:
                for alert in alerts:
                    st.error(alert['message'])
            else:
                st.success("No students are currently at high risk.")
        else:
            st.info("No prediction data to run alerts on.")
        
    with tab2:
        st.subheader("Manage Users")
        users = get_all_users()
        if users:
            import pandas as pd
            df = pd.DataFrame(users, columns=["Username", "Role"])
            st.dataframe(df, use_container_width=True)
            
    with tab3:
        st.subheader("Audit Trail")
        st.caption("Recent system actions tracking")
        logs = get_audit_trail()
        if not logs.empty:
            st.dataframe(logs, use_container_width=True)
        else:
            st.info("No audit logs found.")

    with tab4:
        st.subheader("⚙️ System Controls")
        st.write("Execute background tasks and model maintenance.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Backup Database Now", use_container_width=True):
                if backup_database():
                    st.success("✅ Database backup created successfully!")
                else:
                    st.error("❌ Database backup failed.")
                    
        with col2:
            if st.button("🧠 Retrain Prediction Model", use_container_width=True):
                with st.spinner("Retraining model in background..."):
                    if retrain_random_forest():
                        st.success("✅ Model retrained and saved successfully!")
                    else:
                        st.warning("⚠️ Retraining skipped (insufficient data or accuracy drop).")
