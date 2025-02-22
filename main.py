import streamlit as st
import requests
import fitz  # PyMuPDF for better PDF extraction
from langchain_groq import ChatGroq
import tiktoken

# Initialize LLM model (Replace with your API key)
model = ChatGroq(model="llama3-8b-8192", api_key="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")

def count_tokens(text):
    return len(text) // 4

# Function to extract job details using requests
def extract_job_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text  # Returns raw HTML (needs processing)
    except Exception as e:
        return f"Error extracting job details: {str(e)}"


# ✅ Updated Function: Extract text from PDF using PyMuPDF
def extract_resume_text(pdf_file):
    try:
        with open("uploaded_resume.pdf", "wb") as f:
            f.write(pdf_file.read())

        # Open and extract text using PyMuPDF
        doc = fitz.open("uploaded_resume.pdf")
        text = "\n".join([page.get_text("text") for page in doc])

        if not text.strip():
            return "⚠️ No text found! It might be an image-based PDF."

        return text
    except Exception as e:
        return f"Error extracting resume text: {str(e)}"


# Function to analyze job fit using LLM
def analyze_resume(job_desc, resume_text):
    template = """ 
    You are a recruitment expert who analyzes a resume based on the provided job description.

    ### Job Description:
    {desc}

    ### Candidate's Resume:
    {Resume}

    **Rules:** 
    - Minimum qualification (work experience required) must be passed, or else reject immediately.
    - Be strict in evaluation of job fit score.

    ### Evaluation Criteria:
    - **Job Fit Score (0-100%)**: 
    - **Key Strengths**: 
    - **Potential Gaps**: 
    - **Final Recommendation (Hire/Consider/Reject)**: 

    Please provide a structured response strictly in this format.
    """

    prompt = template.format(desc=job_desc, Resume=resume_text)
    response = model.invoke(prompt)
    return response.content


# Streamlit UI
st.title("🔍 AI Job Fit Evaluator")

# User inputs
job_url = st.text_input("📌 Enter Job Listing URL:")
resume_pdf = st.file_uploader("📂 Upload Your Resume (PDF)", type=["pdf"])

if st.button("🚀 Analyze Resume"):
    if job_url and resume_pdf:
        st.write("📡 Extracting job details...")
        job_desc = extract_job_details(job_url)

        # Token limit (set a buffer for model response)
        max_tokens = 6000  # Keep space for response

        # Check the token count
        job_desc_tokens = count_tokens(job_desc)

        if job_desc_tokens > max_tokens:
            # Truncate from the beginning, keeping the last 'max_tokens' worth of characters
            job_desc = job_desc[-max_tokens:]  # Keeps last 4000 characters

        # invoking the model to extract necessary information
        job_desc_extracted = model.invoke(job_desc + "extract the skills, experience, job locations, Role, Responsibility, minimum qualification(if any),work-mode and salary(if mentioned).")
        print(job_desc_extracted.content)
        st.write("📜 Extracting resume content...")
        resume_text = extract_resume_text(resume_pdf)

        if "Error" not in job_desc and "Error" not in resume_text:
            st.write("⚡ Analyzing Resume Fit...")
            result = analyze_resume(job_desc_extracted.content, resume_text)
            st.subheader("📊 Evaluation Result")
            st.write(result)
        else:
            st.error("❌ There was an issue processing the data. Please check the inputs.")
    else:
        st.warning("⚠️ Please provide both the job listing URL and a resume PDF.")
