import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.send_mail import send_email, send_reset_password_email

@patch("smtplib.SMTP")
def test_send_email_success(mock_smtp):
    """
    Verifies that the email dispatch system correctly orchestrates 
    SMTP calls for performance reports.
    """
    # Setup mock
    mock_instance = mock_smtp.return_value
    
    # Mock data
    data = {
        "student_id": "STU123456",
        "study_hours": 4.5,
        "attendance": 85,
        "mental_health": 8,
        "sleep_hours": 7.5,
        "exam_scores": 70,
        "email": "student@example.com"
    }
    prediction = 75.0
    
    # Execute
    send_email(data, prediction)
    
    # Assert
    assert mock_smtp.called
    assert mock_instance.starttls.called
    assert mock_instance.login.called
    assert mock_instance.send_message.called
    assert mock_instance.quit.called

@patch("smtplib.SMTP")
def test_send_reset_password_email_success(mock_smtp):
    """
    Verifies that password reset emails are correctly structured 
    and dispatched via secure SMTP.
    """
    # Setup mock
    mock_instance = mock_smtp.return_value
    
    # Execute
    success, msg = send_reset_password_email("user@example.com", "http://test-link")
    
    # Assert
    assert success is True
    assert "sent successfully" in msg
    assert mock_smtp.called
    assert mock_instance.send_message.called

@patch("smtplib.SMTP")
def test_send_email_no_receiver(mock_smtp):
    """
    Ensures the system fails gracefully if no receiver email is provided.
    """
    # Mock data with no email/student_id
    data = {"study_hours": 4}
    
    # Execute
    send_email(data, 70.0)
    
    # Assert
    assert not mock_smtp.called

@patch("smtplib.SMTP")
def test_send_email_smtp_error(mock_smtp):
    """
    Verifies robust error handling when the SMTP server is unreachable.
    """
    # Setup mock to raise error
    mock_smtp.side_effect = Exception("SMTP Server Down")
    
    # Mock complete data set to reach SMTP call
    data = {
        "student_id": "S1", 
        "email": "test@test.com",
        "study_hours": 4,
        "attendance": 80,
        "mental_health": 5,
        "sleep_hours": 6,
        "exam_scores": 60
    }
    
    # Execute (should not raise due to try-except in send_email)
    send_email(data, 60.0)
    
    # Assert
    assert mock_smtp.called
