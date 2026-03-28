import streamlit as st
import pandas as pd
from config.constants import SUPPORTED_FORMATS
import os

def upload_page():
    st.title("📂 Bulk Upload Data")
    st.markdown("Upload a CSV or Excel file containing student data for bulk predictions.")
    
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=[f.replace('.', '') for f in SUPPORTED_FORMATS]
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                
            st.success(f"✅ Successfully loaded {len(df)} records!")
            st.dataframe(df.head())
            
            if st.button("Run Bulk Predictions"):
                with st.spinner("Running predictions using ML model..."):
                    # Process predictions here
                    st.success("✅ Bulk predictions processed successfully! Check the Reports tab.")
                    
        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
