import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# 1. Load the Secure Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Page Config (Premium Look)
st.set_page_config(page_title="JobFit Pro", layout="wide", page_icon="💼")
st.title("💼 JobFit Pro: AI Career Consultant")
st.markdown("### Professional Resume & Interview Coach") # <--- REMOVED "Free Tier" text

# 3. Helper: Extract text from PDF
def get_pdf_text(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# 4. Feature 1: Resume Analysis
def analyze_resume(resume_text, job_description):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0, google_api_key=api_key)
    template = """
    Act as a Senior Technical Recruiter.
    Compare the Resume to the Job Description (JD).
    
    RESUME: {resume_text}
    JD: {job_description}
    
    Output a professional report:
    1. **Match Score**: (0-100%)
    2. **Missing Keywords**: (Crucial skills missing from resume)
    3. **Profile Summary**: (Professional assessment)
    4. **Actionable Tips**: (3 specific changes to get hired)
    """
    prompt = PromptTemplate(input_variables=["resume_text", "job_description"], template=template)
    chain = prompt | llm
    return chain.invoke({"resume_text": resume_text, "job_description": job_description}).content

# 5. Feature 2: Cover Letter
def generate_cover_letter(resume_text, job_description):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5, google_api_key=api_key)
    template = """
    Write a persuasive cover letter for this candidate.
    RESUME: {resume_text}
    JOB DESCRIPTION: {job_description}
    
    Requirements:
    - Professional tone
    - Highlight top 2 achievements from resume
    - Explain why they fit the JD
    - Under 250 words
    """
    prompt = PromptTemplate(input_variables=["resume_text", "job_description"], template=template)
    chain = prompt | llm
    return chain.invoke({"resume_text": resume_text, "job_description": job_description}).content

# 6. Feature 3: Mock Interview Question (NEW!)
def generate_interview_question(resume_text, job_description):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, google_api_key=api_key)
    template = """
    Based on the resume and job description, generate ONE tough interview question 
    that a hiring manager would ask this specific candidate.
    
    RESUME: {resume_text}
    JD: {job_description}
    
    Output ONLY the question.
    """
    prompt = PromptTemplate(input_variables=["resume_text", "job_description"], template=template)
    chain = prompt | llm
    return chain.invoke({"resume_text": resume_text, "job_description": job_description}).content

# 7. UI Layout
# We use "Tabs" to organize the features cleanly
tab1, tab2, tab3 = st.tabs(["📊 Resume Analysis", "📝 Cover Letter", "🎤 Mock Interview"])

# Global Inputs (Sidebar)
with st.sidebar:
    st.header("📂 Applicant Data")
    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type="pdf")
    job_desc = st.text_area("Paste Job Description", height=300)

# LOGIC: Resume Analysis
with tab1:
    st.header("Resume Evaluation")
    if st.button("Analyze Match"):
        if uploaded_resume and job_desc:
            with st.spinner("Analyzing..."):
                text = get_pdf_text(uploaded_resume)
                result = analyze_resume(text, job_desc)
                st.markdown(result)
        else:
            st.warning("Please upload a resume and JD first.")

# LOGIC: Cover Letter
with tab2:
    st.header("Cover Letter Draft")
    if st.button("Generate Letter"):
        if uploaded_resume and job_desc:
            with st.spinner("Writing..."):
                text = get_pdf_text(uploaded_resume)
                result = generate_cover_letter(text, job_desc)
                st.markdown(result)
        else:
            st.warning("Please upload a resume and JD first.")

# LOGIC: Mock Interview
with tab3:
    st.header("Interview Prep")
    if st.button("Generate Interview Question"):
        if uploaded_resume and job_desc:
            with st.spinner("Generating question..."):
                text = get_pdf_text(uploaded_resume)
                question = generate_interview_question(text, job_desc)
                st.info(f"🗣️ **Interviewer asks:** {question}")
                
                # Optional: Text area for user to answer (Non-functional in this demo, but good UI)
                st.text_area("Type your answer here to practice:")
        else:
            st.warning("Please upload a resume and JD first.")
