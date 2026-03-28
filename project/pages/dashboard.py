import streamlit as st

def dashboard():
    st.markdown("<h1 style='text-align: center; color: #f8fafc;'>📊 Student Performance Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # User info
    email = st.session_state.get("user", "User")
    role = st.session_state.get("role", "student").lower()

    if role == "staff" or role == "admin":
        st.markdown(f"<div class='card'><h3>Welcome back, {email}! 👨‍🏫</h3><p style='color:#94a3b8;'>Here is the university overview.</p></div>", unsafe_allow_html=True)
        
        # Admin / Staff KPI Cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Tracked Students", value="1,240", delta="12% vs Last Term")
        with col2:
            st.metric(label="Average Attendance", value="85%", delta="-2%", delta_color="inverse")
        with col3:
            st.metric(label="Average Predicted Score", value="78", delta="+5", delta_color="normal")
            
        st.markdown("<br><div class='card'><h4>💡 Quick Action</h4><p>Navigate to Analytics to view detailed visualizations of student data, or the Reports section to download bulk data.</p></div>", unsafe_allow_html=True)

    else:
        st.markdown(f"<div class='card'><h3>Welcome, {email}! 🎓</h3><p style='color:#94a3b8;'>Stay on track with your goals.</p></div>", unsafe_allow_html=True)
        
        # Student KPI Cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Current Semester Target", value="85%", delta="On track")
        with col2:
            st.metric(label="Upcoming Exams", value="2")
        with col3:
            st.metric(label="Recent Achievements", value="3", delta="+1 this week")

        st.markdown("<br><div class='card'><h4>🎯 What's Next?</h4><p>Visit the Prediction tab to test scenarios for your upcoming exams and see what scores you might achieve based on study habits.</p></div>", unsafe_allow_html=True)
