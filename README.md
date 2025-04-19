# Automated CV Scoring and Feedback AI Agent

## Project Overview
This project automates the process of collecting resumes from emails, extracting relevant information, scoring them based on the job description, and providing personalized feedback to candidates via email. The agent uses the Gmail API for email interaction and processes resumes in PDF and DOCX formats. The feedback includes details on AI experience, CV score, and job description match score.

## Features
- **Resume Collection:** Collects unread resumes from Gmail inbox.
- **Resume Scoring:** Scores the resumes based on predefined criteria (AI experience, skills, job description match).
- **Email Automation:** Sends personalized feedback to candidates via email.
- **Logging:** Tracks processed resumes with a timestamp and stores them in a CSV file.

## Code Structure
- `email_collector.py`: Handles Gmail API integration to collect resumes from emails.
- `email_sender.py`: Sends feedback emails to candidates.
- `gmail_auth.py`: Handles Gmail OAuth authentication.
- `logging_custom.py`: Logs processed resumes to a CSV file.
- `resume_scoring.py`: Extracts resume information, including skills, experience, and education, and scores them.
- `main.py`: The main script that automates the entire process.

## Installation

### 1️⃣ Clone this repository:
```bash
git clone https://gitlab.com/your-repo-url.git
cd your-repo

2️⃣ Create a Virtual Environment & Install Dependencies
$ python -m venv venv
$ On Windows: venv\Scripts\activate
$ pip install -r requirements.txt


3️⃣ Set up Gmail API
Follow these steps to enable the Gmail API and set up OAuth authentication:

Step 1: Go to Google Cloud Console
Navigate to the Google Cloud Console.

If you don't have a Google Cloud account, you may need to create one.

Step 2: Create a New Project
In the Google Cloud Console, click on the project dropdown (near the top of the page) and click on New Project.

Give your project a name (e.g., "CV Scoring AI Agent") and select your billing account if prompted.

Click Create.

Step 3: Enable Gmail API
With your new project selected, navigate to the API & Services section on the left-hand sidebar.

Click on Library.

In the search bar, type "Gmail API" and select it from the results.

Click Enable to enable the Gmail API for your project.

Step 4: Create OAuth 2.0 Credentials
After enabling the Gmail API, you'll need to create OAuth credentials to interact with the API.

In the APIs & Services dashboard, click on Credentials on the left-hand menu.

Click on the Create Credentials button and select OAuth 2.0 Client ID.

Step 5: Configure OAuth Consent Screen
If this is your first time using OAuth 2.0, you may need to configure the consent screen. This is what users will see when they authenticate your app with Gmail.

Click on OAuth consent screen.

Choose External for the user type.

Fill in the required fields:

App name: Enter a name for your app (e.g., "Automated CV Scoring").

User support email: Your email address.

Developer contact information: Your email.

Click Save and Continue to proceed.

Step 6: Create OAuth Credentials
After configuring the consent screen, go back to the Credentials page.

Click Create Credentials and choose OAuth 2.0 Client ID again.

Under Application type, select Desktop app.

Name your credentials (e.g., "CV Scoring App OAuth").

Click Create.

A popup will appear with your Client ID and Client Secret. Click Download to get the credentials.json file.

Step 7: Download credentials.json
Save the credentials.json file to the root of your project directory.

This file will allow your application to authenticate with Gmail API.

Step 8: Authorize the Application
To authenticate your Gmail account and generate the token.json file, run the following command in your terminal:


python gmail_auth.py

This will open a browser window prompting you to sign in to your Google account.

Once signed in, allow the app to access your Gmail account.

The script will save the token.json file, which is used for making API requests without needing to log in again.

4️⃣ Run the Agent
Once the Gmail API is set up, you can run the agent with the following command:

python main.py


Usage
Resume Collection
The script collects resumes from Gmail and saves them in the resumes/ directory.

Resume Scoring
Resumes are scored based on AI experience, skills, and job description match.

Email Feedback
Feedback emails are sent to the candidates with their CV score and job description match percentage.
