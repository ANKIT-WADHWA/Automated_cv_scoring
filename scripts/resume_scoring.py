import re
import pdfplumber
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------- Preprocessing -------------------- #
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -------------------- Resume Extraction -------------------- #
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting from {pdf_path}: {e}")
        return ""

def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        print(f"Error extracting from {docx_path}: {e}")
        return ""

# -------------------- Identity Extraction -------------------- #
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Not found"

def mask_email(email):
    return re.sub(r'(?<=.).(?=[^@]*?@)', '*', email)

def extract_name(text):
    lines = text.split('\n')
    for line in lines[:5]:
        words = line.strip().split()
        if 1 <= len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
            return line.strip()
    return "Not found"

def mask_name(name):
    parts = name.split()
    return ' '.join(p[0] + '*'*(len(p)-2) + p[-1] if len(p) > 2 else p for p in parts) if len(parts) >= 2 else name

# -------------------- Experience & Skills -------------------- #
def has_ai_experience(text):
    keywords = ["machine learning", "deep learning", "neural network", "AI", "nlp", "cv", "computer vision", "data science"]
    text = text.lower()
    return any(keyword in text for keyword in keywords)

def extract_work_experience(text):
    keywords = ["experience", "worked", "responsible", "role", "position", "intern", "employed", "job", "project", "handled", "managed", "engineer", "developer", "contributed"]
    text = preprocess_text(text)
    
    # Improved logic: Count how many separate tasks or roles are mentioned
    work_experience_count = 0
    for keyword in keywords:
        work_experience_count += text.count(keyword)
    
    return work_experience_count

def extract_education(text):
    keywords = ["bachelor", "master", "degree", "phd", "university"]
    text = preprocess_text(text)
    return any(keyword in text for keyword in keywords)

def extract_skills(text):
    keywords = ["python", "java", "c++", "machine learning", "data science", "ai", "deep learning", "neural network", "nlp", 
                "sql", "tensorflow", "keras", "pandas", "numpy", "scikit-learn", "data analysis", "flask", "django", 
                "matplotlib", "seaborn", "linux", "git"]
    text = preprocess_text(text)
    return sum(1 for keyword in keywords if keyword in text)

# -------------------- JD-CV Matching -------------------- #
def calculate_match(jd_text, resume_text):
    jd_text = preprocess_text(jd_text)
    resume_text = preprocess_text(resume_text)
    
    # Increase JD title length by considering longer titles or full job description
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3))  # Use n-grams for better matching
    tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
    
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

# -------------------- Final Scoring & Aggregation -------------------- #
def extract_resume_info(resume_text, job_description):
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    masked_name = mask_name(name)
    masked_email = mask_email(email)

    ai_exp = "Yes" if has_ai_experience(resume_text) else "No"
    jd_score_raw = calculate_match(job_description, resume_text) * 100  # Raw JD-CV match score (0-100 scale)
    work_exp_count = extract_work_experience(resume_text)
    has_education = "Yes" if extract_education(resume_text) else "No"
    skill_count = extract_skills(resume_text)

    # Adjust scoring based on the maximum points and provide the final score
    jd_score = min(jd_score_raw * 10, 20)  # JD score, max 20 points
    work_score = min(work_exp_count * 1, 10)  # Work experience score, max 20 points
    skills_score = min(skill_count * 2.5, 50)  # Skills score, max 40 points
    ai_score = 10 if ai_exp == "Yes" else 0  # AI experience score, max 10 points
    edu_score = 10 if has_education == "Yes" else 0  # Education score, max 10 points

    # Total score calculation
    total_score = min(jd_score + work_score + skills_score + ai_score + edu_score, 100)

    # Return results in the required format
    return {
        "name": name,
        "masked_name": masked_name,
        "email": email,
        "masked_email": masked_email,
        "ai_experience": ai_exp,
        "jd_cv_match_score": round(jd_score_raw, 2),  # Showing raw JD score
        "education": has_education,
        "skills_count": skill_count,
        "cv_score": round(total_score, 2)  # Total score (out of 100)
    }

# -------------------- Default Job Description -------------------- #
def get_default_job_description():
    """
    Returns the predefined Job Description for AI Intern.
    """
    jd_text = """
    Job Title: AI Intern

    Job Description:
    We are looking for an AI Intern to assist in developing and deploying machine learning models. The ideal candidate should have a background in machine learning, deep learning, and data science. Responsibilities will include data preprocessing, model training, and assisting in the development of AI systems.

    Requirements:
    - Strong understanding of machine learning algorithms.
    - Experience with Python and machine learning libraries like TensorFlow and PyTorch.
    - Ability to work with large datasets.
    - Strong problem-solving and communication skills.
    - Currently enrolled in a relevant degree program (B.Tech, M.Tech, etc.).

    Skills:
    - Python
    - Machine Learning,ML
    - Deep Learning,DL
    - Data Science,DS
    - TensorFlow, PyTorch, Scikit-learn
    """
    return jd_text

# -------------------- Main Program -------------------- #

if __name__ == "__main__":
    # Load predefined Job Description (AI Intern)
    job_description = get_default_job_description()

    # Get the path of the resume (PDF/DOCX)
    resume_path = input("Enter the path of the resume (PDF/DOCX): ")

    # Extract text from the resume (PDF/DOCX)
    if resume_path.endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_path.endswith('.docx'):
        resume_text = extract_text_from_docx(resume_path)
    else:
        print("Unsupported file format. Please provide a PDF or DOCX file.")
        exit()

    # Process the resume with JD and display results
    result = extract_resume_info(resume_text, job_description)
    
    # Display the results
    print("\nResume Scoring Results:")
    for key, value in result.items():
        print(f"{key}: {value}")
