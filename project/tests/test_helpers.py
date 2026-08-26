import sys
import os
import pytest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.helpers import calculate_trend, get_feedback_sentiment, format_percent

from utils.logger import log_event

def test_calculate_trend():
    assert calculate_trend(85.0, 70.0) == "↑ Improving"
    assert calculate_trend(50.0, 75.0) == "↓ Declining"
    assert calculate_trend(60.0, 61.0) == "→ Stable"
    assert calculate_trend(60.0, None) == "NEW"

def test_get_feedback_sentiment():
    assert get_feedback_sentiment("This app is great! It helped me a lot.") == "Positive"
    assert get_feedback_sentiment("I struggle with this, it's very difficult.") == "At Risk"
    assert get_feedback_sentiment("This is a simple student prediction app.") == "Neutral"

def test_format_percent():
    assert format_percent(85.567) == "85.6%"
    assert format_percent("invalid") == "N/A"

def test_log_event():
    # Test that logging doesn't crash (non-blocking)
    try:
        log_event("TEST_UNIT", "pytest", {"status": "ok"})
    except Exception as e:
        pytest.fail(f"Logger malfunction: {e}")

if __name__ == "__main__":
    test_calculate_trend()
    test_get_feedback_sentiment()
    test_format_percent()
    test_log_event()
    print("Helper and Logger integrity tests passed!")
