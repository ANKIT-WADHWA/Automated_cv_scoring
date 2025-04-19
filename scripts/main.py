import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from email_collector import collect_resumes
from email_sender import send_email, generate_feedback_email
from logging_custom import log_processed_resume
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from config import SCOPES  # Import scopes from config

def automate_processing():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    while True:
        resume_info = collect_resumes()
        if resume_info:
            feedback = generate_feedback_email(resume_info)
            recipient_email = resume_info['email']
            subject = f"📄 Resume Feedback – Your CV Score is {resume_info['cv_score']}!"
            send_email(service, recipient_email, subject, feedback)
            log_processed_resume(resume_info, "path_to_resume_file")

        time.sleep(10)

if __name__ == '__main__':
    automate_processing()
