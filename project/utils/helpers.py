import json
import os
from datetime import datetime

# 🎨 Lottie Animations
def load_lottie(path):
    """Safely loads a JSON lottie file."""
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def show_lottie_anim(st_obj, path, height=200, key=None):
    """Displays a lottie animation if Streamlit Lottie is available."""
    try:
        from streamlit_lottie import st_lottie
        animation = load_lottie(path)
        if animation:
            st_lottie(animation, height=height, key=key)
    except Exception:
        pass

# 📊 Data Formatting
def format_percent(val):
    """Formats a number as a percentage string (1 decimal)."""
    try:
        return f"{float(val):.1f}%"
    except (ValueError, TypeError):
        return "N/A"

def get_score_label(score):
    """Returns a textual performance label based on score."""
    if score >= 80: return "Excellent"
    if score >= 60: return "Good"
    if score >= 40: return "Average"
    return "At Risk"

# 🕐 Time Functions
def get_now():
    """Returns standardized timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_date_human(date_str):
    """Converts DB timestamp to a cleaner display format."""
    if not date_str: return "Never"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %H:%M")
    except Exception:
        return str(date_str).split(" ")[0]

# 🧪 ANALYTICS HELPERS
def calculate_trend(current, previous):
    """Calculates if performance is Improving, Stable, or Declining."""
    if previous is None or previous == 0: return "NEW"
    diff = current - previous
    if diff > 3: return "↑ Improving"
    if diff < -3: return "↓ Declining"
    return "→ Stable"

def get_feedback_sentiment(text):
    """Simple keyword-based sentiment detection for student feedback."""
    if not text: return "N/A"
    text = text.lower()
    pos = ["good", "great", "excellent", "happy", "helped", "improved", "easy"]
    neg = ["bad", "poor", "difficult", "struggle", "confused", "hard", "slow"]
    
    pos_score = sum(1 for word in pos if word in text)
    neg_score = sum(1 for word in neg if word in text)
    
    if pos_score > neg_score: return "Positive"
    if neg_score > pos_score: return "At Risk"
    return "Neutral"