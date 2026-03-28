import smtplib
from email.mime.text import MIMEText

def send_email(data, prediction):

    sender_email = "studentperformanceprediction1@gmail.com"      # change
    app_password = "cngufosjfqhyitbv"        # change
    tutor_email = "dhatchinamoorthys006@gmail.com"           # change

    subject = "Student Performance Prediction Report"

    body = f"""
Student Performance Prediction Details

Study Hours : {data['study_hours']}
Attendance : {data['attendance']}
Mental Health : {data['mental_health']}
Sleep Hours : {data['sleep_hours']}
Previous Score : {data['exam_scores']}

Predicted Performance : {prediction:.2f} %
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = tutor_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()