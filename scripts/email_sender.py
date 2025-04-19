import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send an email
def send_email(service, to, subject, body):
    try:
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message = service.users().messages().send(userId="me", body={'raw': raw_message}).execute()

        print(f"📧 Email sent to {to} with subject: {subject}")
    except HttpError as error:
        print(f"❌ An error occurred while sending email: {error}")


# Function to generate the feedback email body
def generate_feedback_email(resume_info):
    name = resume_info["name"]  # Use actual name
    ai_experience = resume_info["ai_experience"]
    jd_match_score = resume_info["jd_cv_match_score"]
    cv_score = resume_info["cv_score"]

    feedback_body = f"""
Hello {name},

Thank you for submitting your resume for the job application. Here is the feedback based on the job description and your CV:

📌 AI Experience: {ai_experience}
📈 JD Match Score: {jd_match_score}%
⭐ CV Score: {cv_score}/100

We will get back to you shortly after reviewing all applications.

Best regards,  
HR Team
    """
    return feedback_body
