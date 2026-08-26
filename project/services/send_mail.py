import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(data, prediction, file_path=None):
    try:
        # 🔐 Use environment variables or fallback to hardcoded auth
        sender_email = os.getenv("EMAIL_SENDER", os.getenv("EMAIL_USER", ""))
        app_password = os.getenv("EMAIL_PASSWORD", os.getenv("EMAIL_PASS", ""))

        # 📩 Send to logged-in user (better)
        receiver_email = data.get("email", data.get("student_id"))

        if not receiver_email:
            print("⚠️ No email provided")
            return

        # -------------------------------
        # 📧 EMAIL CONTENT
        # -------------------------------
        subject = "📊 Student Performance Prediction Report"

        body = f"""
Student Performance Prediction Details

🆔 Student ID : {data['student_id']}

📘 Study Hours : {data['study_hours']}
📊 Attendance : {data['attendance']}%
🧠 Mental Health : {data['mental_health']}
😴 Sleep Hours : {data['sleep_hours']}
📝 Previous Score : {data['exam_scores']}

🎯 Predicted Performance : {prediction:.2f} %
"""

        # -------------------------------
        # 📦 CREATE MESSAGE
        # -------------------------------
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        msg.attach(MIMEText(body, "plain"))

        # -------------------------------
        # 📎 ATTACH FILE (OPTIONAL)
        # -------------------------------
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_part = MIMEApplication(f.read(), Name=os.path.basename(file_path))

            file_part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
            msg.attach(file_part)

        # -------------------------------
        # 🚀 SEND EMAIL
        # -------------------------------
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:
        print(f"❌ Email error: {e}")

def send_reset_password_email(receiver_email, reset_link="https://student-performance.example.com/reset"):
    try:
        sender_email = os.getenv("EMAIL_SENDER", os.getenv("EMAIL_USER", ""))
        app_password = os.getenv("EMAIL_PASSWORD", os.getenv("EMAIL_PASS", ""))
        
        subject = "🔐 Password Reset Request"
        body = f"Hello,\n\nYou requested a password reset for your account.\nClick the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, please ignore this email."
        
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg.attach(MIMEText(body, "plain"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)
