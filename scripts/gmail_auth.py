import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add root to path

from config import SCOPES

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def main():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the credentials as token.json
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    # Test the connection
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])

    print(f"You have {len(messages)} unread emails.")

if __name__ == '__main__':
    main()
