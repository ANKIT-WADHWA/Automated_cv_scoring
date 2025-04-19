# Automated CV Scoring and Feedback AI Agent
```bash
with the live demo screenshots attached
```
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
```
### 2️⃣ Create a Virtual Environment & Install Dependencies
```bash
$ python -m venv venv
$ On Windows: venv\Scripts\activate
$ pip install -r requirements.txt
```


### 3️⃣ Set up Gmail API
Follow these steps to enable the Gmail API and set up OAuth authentication:

🔹 Step 1: Go to Google Cloud Console
Open Google Cloud Console.

Sign in with your Google account.

🔹 Step 2: Create a New Project
Click the project dropdown (top-left corner) → New Project

Enter a name (e.g., CV Scoring AI Agent) → Click Create

🔹 Step 3: Enable Gmail API
Navigate to:
```bash
APIs & Services → Library
```
Search for Gmail API

Click it → Click Enable

🔹 Step 4: Configure OAuth Consent Screen
Go to:
``` bash
APIs & Services → OAuth consent screen
```
Choose External → Click Create

Fill in:

App name: Automated CV Scoring

User support email: your email

Developer contact info: your email

Click Save and Continue until done

🔹 Step 5: Create OAuth 2.0 Credentials
Go to:
```bash
APIs & Services → Credentials
```
Click Create Credentials → Select OAuth Client ID

Choose Application type: Desktop App

Name it (e.g., CV Scoring App OAuth) → Click Create

Click Download to get credentials.json

🔹 Step 6: Add credentials.json to Your Project
```bash
# Move the file to the root of your project directory
```
🔹 Step 7: Authorize the Application
```bash
# Run the Gmail authentication script
python gmail_auth.py
```
A browser will open → Log in to your Google account

Allow the required permissions

token.json will be created for future Gmail access
This will open a browser window prompting you to sign in to your Google account.

Once signed in, allow the app to access your Gmail account.

The script will save the token.json file, which is used for making API requests without needing to log in again.

### 4️⃣ Run the Agent
```bash
Once the Gmail API is set up, you can run the agent with the following command:
python main.py
```

### Usage
```bash
Resume Collection
The script collects resumes from Gmail and saves them in the resumes/ directory.

Resume Scoring
Resumes are scored based on AI experience, skills, and job description match.

Email Feedback
Feedback emails are sent to the candidates with their CV score and job description match percentage.
```