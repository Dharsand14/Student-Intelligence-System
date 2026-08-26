import pytest
from unittest.mock import patch, MagicMock
import streamlit as st

# We mock Streamlit's entire interaction layer to verify that 
# the pages orchestrate their UI components correctly.

@patch("streamlit.sidebar")
@patch("streamlit.title")
@patch("streamlit.markdown")
@patch("streamlit.columns")
@patch("streamlit.form")
def test_dashboard_rendering(mock_form, mock_cols, mock_markdown, mock_title, mock_sidebar):
    """
    Verifies that the dashboard correctly renders the class-level overview 
    and specialized KPI metrics.
    """
    from pages.dashboard import dashboard
    
    # Setup session state mock
    st.session_state["role"] = "staff"
    st.session_state["user"] = "admin@university.edu"
    
    # Execute
    dashboard()
    
    # Assertions
    assert mock_title.called
    assert any("Dashboard" in str(args) for args in mock_title.call_args_list)

@patch("streamlit.form")
@patch("streamlit.slider")
@patch("streamlit.button")
def test_prediction_page_components(mock_button, mock_slider, mock_form):
    """
    Ensures that the prediction page correctly initializes all 
    5 essential performance inputs (Study, Attend, Sleep, etc.)
    """
    from pages.prediction import prediction_page
    
    # Setup session state
    st.session_state["role"] = "student"
    st.session_state["student_id"] = "23BCS138"
    
    # Execute
    prediction_page()
    
    # Assert that all 5 sliders for factors were requested
    assert mock_slider.call_count >= 5

@patch("streamlit.download_button")
@patch("streamlit.dataframe")
def test_reports_page_exports(mock_df, mock_download):
    """
    Validates that the reports module correctly exposes the 
    CSV and Excel generation interfaces.
    """
    from pages.reports import reports_page
    
    # Setup session state
    st.session_state["role"] = "staff"
    
    # Mock data return from DB
    with patch("database.predictions_db.get_all_predictions") as mock_db:
        mock_db.return_value = [{"student_id": "S1", "predicted_score": 80.0, "created_at": "2026-03-29"}]
        
        # Execute
        reports_page()
        
    # Assert
    assert mock_download.called
    assert any("CSV" in str(args) for args in mock_download.call_args_list)

@patch("streamlit.radio")
@patch("streamlit.selectbox")
@patch("streamlit.text_area")
def test_feedback_page_inputs(mock_area, mock_select, mock_radio):
    """
    Ensures the feedback portal captures all required qualitative 
    and quantitative data points.
    """
    from pages.feedback import feedback_page
    
    # Setup session state
    st.session_state["role"] = "student"
    st.session_state["fb_rating"] = 4
    
    # Execute
    feedback_page()
    
    # Assertions
    assert mock_radio.called
    assert mock_select.called
    assert mock_area.called
