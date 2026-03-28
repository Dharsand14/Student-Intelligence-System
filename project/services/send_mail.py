import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(data, prediction, file_path=None):
    try:
        # 🔐 Use environment variables (IMPORTANT)
        sender_email = os.getenv("studentperformanceprediction1@gmail.com")
        app_password = os.getenv("cngufosjfqhyitbv")

        # 📩 Send to logged-in user (better)
        receiver_email = data.get("studentperformanceprediction1@gmail.com")

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