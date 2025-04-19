import csv
from datetime import datetime

def log_processed_resume(resume_info, file_path):
    with open('processed_resumes.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'email', 'ai_experience', 'jd_match_score', 'cv_score', 'timestamp', 'file_path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'name': resume_info["masked_name"],
            'email': resume_info["masked_email"],
            'ai_experience': resume_info["ai_experience"],
            'jd_match_score': resume_info["jd_cv_match_score"],
            'cv_score': resume_info["cv_score"],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_path': file_path
        })
        print(f"Logged resume data for {resume_info['masked_name']}")
