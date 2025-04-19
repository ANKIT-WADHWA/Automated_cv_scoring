import os
import base64
import re
import html
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from resume_scoring import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_resume_info
)
from email_sender import send_email, generate_feedback_email
from logging_custom import log_processed_resume  # Added logging

DOWNLOAD_DIR = "resumes"
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify']  # Updated SCOPES
JOB_DESCRIPTION = "We are looking for someone with experience in Python, ML, and DS."
MAX_FILENAME_LENGTH = 255

creds = Credentials.from_authorized_user_file('token.json', SCOPES)

def sanitize_filename(filename):
    filename = html.unescape(filename)
    filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    filename = filename.replace(" ", "_")
    return filename[:MAX_FILENAME_LENGTH]

def save_attachment(service, msg, msg_id):
    payload = msg.get('payload', {})
    parts = payload.get('parts', [])

    for part in parts:
        filename = part.get("filename")
        mimeType = part.get("mimeType")
        body = part.get("body", {})

        if filename and mimeType and (
            'application/pdf' in mimeType or
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in mimeType
        ):
            attachment_id = body.get("attachmentId")
            if attachment_id:
                attachment = service.users().messages().attachments().get(
                    userId="me", messageId=msg_id, id=attachment_id
                ).execute()

                file_data = base64.urlsafe_b64decode(attachment['data'])
                safe_filename = sanitize_filename(filename)
                file_path = os.path.join(DOWNLOAD_DIR, f"{msg_id}_{safe_filename}")

                counter = 1
                base_path, ext = os.path.splitext(file_path)
                while os.path.exists(file_path):
                    file_path = f"{base_path}_{counter}{ext}"
                    counter += 1

                with open(file_path, 'wb') as f:
                    f.write(file_data)

                print(f"[✓] Downloaded: {file_path}")
                return file_path

    return None

def collect_resumes():
    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            print("[!] No unread emails found.")
            return None  # Changed from empty list to None to avoid breaking email feedback generation

        resume_found = False
        for message in messages[:5]:  # Process up to 5 unread emails
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            file_path = save_attachment(service, msg, message['id'])

            if file_path:
                resume_found = True
                print(f"\n📄 Processing: {file_path}")
                text = ""
                if file_path.endswith('.pdf'):
                    text = extract_text_from_pdf(file_path)
                elif file_path.endswith('.docx'):
                    text = extract_text_from_docx(file_path)

                resume_info = extract_resume_info(text, JOB_DESCRIPTION)

                print("🔍 Resume Info:")
                for key, val in resume_info.items():
                    print(f"{key}: {val}")
                print("\n" + "-"*50 + "\n")

                # Send email feedback after processing the resume
                feedback_body = generate_feedback_email(resume_info)
                send_email(service, resume_info["email"], "Your Resume Feedback", feedback_body)
                log_processed_resume(resume_info, file_path)  # Log the processed resume with correct file path

                # Mark the email as read by removing the 'UNREAD' label
                msg_labels = {'removeLabelIds': ['UNREAD']}
                service.users().messages().modify(userId='me', id=message['id'], body=msg_labels).execute()

        if not resume_found:
            print("[!] No resumes found in unread emails.")
            return None  # Return None if no resume was found

    except HttpError as error:
        print(f"[✗] An error occurred: {error}")
        return None  # In case of an error, return None

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    collect_resumes()
