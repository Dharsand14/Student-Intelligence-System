import streamlit as st
from database.feedback_db import add_feedback, get_all_feedback


STAR_LABELS = {1: "Poor", 2: "Fair", 3: "Good", 4: "Very Good", 5: "Excellent"}
STAR_EMOJIS = {1: "😞", 2: "😐", 3: "🙂", 4: "😊", 5: "🤩"}
CATEGORIES = ["Overall Experience", "Prediction Accuracy", "UI / Design", "Ease of Use", "Suggestions"]


def feedback_page():
    st.markdown("""
    <style>
    .star-row { display: flex; gap: 6px; justify-content: center; margin: 12px 0; }
    .star-btn {
        background: none; border: none; font-size: 2.6rem; cursor: pointer;
        transition: transform 0.15s ease, filter 0.15s ease;
        filter: grayscale(1) opacity(0.4);
        line-height: 1;
    }
    .star-btn:hover, .star-btn.active { filter: none; transform: scale(1.25); }
    .star-btn.active { filter: drop-shadow(0 0 8px #fbbf24); }
    .rating-label {
        text-align: center; font-size: 1.1rem; font-weight: 600;
        color: #fbbf24; margin-bottom: 8px; min-height: 1.5em;
    }
    .feedback-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid #4f46e5;
        border-radius: 14px; padding: 20px 24px; margin-bottom: 14px;
    }
    .feedback-meta { font-size: 0.8rem; color: #a5b4fc; margin-bottom: 6px; }
    .feedback-text { font-size: 0.97rem; color: #e0e7ff; }
    .stars-display { color: #fbbf24; font-size: 1.1rem; letter-spacing: 2px; }
    .section-title {
        font-size: 1.4rem; font-weight: 700; color: #c7d2fe;
        border-left: 4px solid #6366f1; padding-left: 12px; margin: 24px 0 14px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("💬 Feedback Center")
    st.markdown("Your feedback helps improve the Student Performance System. Rate and share your thoughts below.")

    st.markdown('<div class="section-title">⭐ Rate Your Experience</div>', unsafe_allow_html=True)

    # --- Star Rating using session state ---
    if "fb_rating" not in st.session_state:
        st.session_state.fb_rating = 0

    cols = st.columns(7)
    star_clicked = None
    with cols[1]:
        st.write("")
    for i, col in enumerate(cols[1:6], start=1):
        with col:
            label = "⭐" if i <= st.session_state.fb_rating else "☆"
            if st.button(label, key=f"star_{i}", help=STAR_LABELS[i], use_container_width=True):
                st.session_state.fb_rating = i
                st.rerun()

    rating = st.session_state.fb_rating
    if rating > 0:
        st.markdown(
            f"<div style='text-align:center;font-size:1.2rem;color:#fbbf24;font-weight:700;margin:4px 0 16px 0'>"
            f"{STAR_EMOJIS[rating]}  {rating}/5 — {STAR_LABELS[rating]}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='text-align:center;color:#6366f1;margin:4px 0 16px 0'>Click a star to rate</div>",
            unsafe_allow_html=True
        )

    # --- Feedback Form ---
    with st.form("feedback_form", clear_on_submit=True):
        category = st.selectbox(
            "📂 Feedback Category",
            CATEGORIES,
            help="Choose the area you want to comment on"
        )

        mood = st.radio(
            "😊 Overall Mood",
            ["😞 Frustrated", "😐 Neutral", "🙂 Satisfied", "🤩 Delighted"],
            horizontal=True
        )

        comments = st.text_area(
            "✍️ Your Comments",
            placeholder="Share what you liked, disliked, or how we can improve...",
            height=120
        )

        col_submit, col_clear = st.columns([2, 1])
        with col_submit:
            submit = st.form_submit_button("🚀 Submit Feedback", use_container_width=True, type="primary")
        with col_clear:
            clear = st.form_submit_button("🔄 Clear Rating", use_container_width=True)

        if clear:
            st.session_state.fb_rating = 0
            st.rerun()

        if submit:
            if rating == 0:
                st.warning("⚠️ Please select a star rating before submitting.")
            else:
                user = st.session_state.get("user", "Anonymous")
                from utils.validation import sanitize_text
                
                # 🛡️ SANITIZE INPUT
                clean_comments = sanitize_text(comments)
                full_comment = f"[{category}] {mood}\n{clean_comments}".strip()
                
                add_feedback(user, full_comment, rating)
                st.session_state.fb_rating = 0
                st.success(f"✅ Thank you! Your **{STAR_LABELS[rating]}** rating has been recorded.")
                st.balloons()

    # --- Previous Feedback History ---
    st.markdown('<div class="section-title">📋 Recent Feedback</div>', unsafe_allow_html=True)

    role = str(st.session_state.get("role", "student")).lower().strip()
    current_user = st.session_state.get("user", "")

    try:
        df = get_all_feedback()
        if df.empty:
            st.info("📭 No feedback submitted yet.")
        else:
            if role != "staff":
                df = df[df["username"] == current_user]

            if df.empty:
                st.info("📭 You haven't submitted any feedback yet.")
            else:
                st.caption(f"Showing {len(df)} feedback record(s)")
                for _, row in df.iterrows():
                    r = int(row.get("rating", 0))
                    stars_html = "⭐" * r + "☆" * (5 - r)
                    user_label = row.get("username", "Unknown")
                    ts = row.get("timestamp", "")
                    text = row.get("feedback_text", "")
                    emoji = STAR_EMOJIS.get(r, "")
                    label = STAR_LABELS.get(r, "")

                    st.markdown(f"""
                    <div class="feedback-card">
                        <div class="feedback-meta">
                            {'👤 ' + user_label + ' &nbsp;|&nbsp; ' if role == 'staff' else ''}
                            🕐 {ts} &nbsp;|&nbsp;
                            <span class="stars-display">{stars_html}</span>
                            &nbsp; {emoji} <strong style="color:#fbbf24">{label}</strong>
                        </div>
                        <div class="feedback-text">{text}</div>
                    </div>
                    """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load feedback history: {e}")
