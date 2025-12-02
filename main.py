import streamlit as st
import google.generativeai as genai
import os
import json
import pandas as pd
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# 1. CONFIGURATION
load_dotenv()
st.set_page_config(
    page_title="JobFit Pro", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# 2. API SETUP
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ API Key missing. Please check your .env file.")
    st.stop()

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.stop()

# 3. SUPERLIST DESIGN (Dark & Red Aesthetic)
st.markdown("""
    <style>
    /* IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');

    /* GLOBAL COLORS */
    .stApp {
        background-color: #0E0E10; /* Deep Charcoal */
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #E0E0E0;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #18181B; 
        border-right: 1px solid #27272A;
    }

    /* ACCENT COLOR (Superlist Red) */
    a { color: #FF5B45 !important; }
    
    /* BUTTONS */
    .stButton > button {
        background-color: #FF5B45 !important;
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 0.6rem 2.5rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 91, 69, 0.3);
    }

    /* HEADERS */
    h1, h2, h3 {
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        color: #FFFFFF !important;
    }
    
    /* SCORE CARD */
    .score-container {
        background-color: #18181B;
        border: 1px solid #333;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .score-title {
        color: #888;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }
    .score-value {
        color: #FF5B45; 
        font-size: 6rem;
        font-weight: 900;
        line-height: 1;
        margin-bottom: 10px;
    }
    .score-sub {
        color: #FFF;
        font-size: 1.5rem;
        font-weight: 600;
    }

    /* ANALYSIS CARDS */
    .analysis-card {
        background-color: #1E1E20;
        border-radius: 16px;
        padding: 25px;
        border: 1px solid #2D2D30;
        margin-bottom: 20px;
    }
    .card-header {
        color: #FF5B45;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* SKILL TAGS */
    .skill-tag {
        display: inline-block;
        background-color: #2D1A1A;
        color: #FF8B7D;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.9rem;
        margin: 0 5px 5px 0;
        border: 1px solid #4A2B2B;
    }
    
    /* RECOMMENDATION BOX */
    .rec-box {
        background-color: #18181B;
        border-left: 4px solid #FF5B45;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 0 12px 12px 0;
    }
    .rec-title {
        color: #FF5B45;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    .rec-body {
        color: #CCCCCC;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* INPUTS */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #18181B !important;
        color: white !important;
        border: 1px solid #27272A !important;
        border-radius: 8px;
    }
    
    /* HIDE MENU */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 4. LOGIC FUNCTIONS
def extract_text(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except: return None

def ask_ai(prompt):
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error: {e}"

def analyze_single_resume(text, job_desc):
    prompt = f"""
    Act as a Senior Career Strategist. Perform a deep-dive analysis of this resume against the JD.
    RESUME: {text}
    JD: {job_desc}

    Return a valid JSON object with these exact keys:
    {{
        "match_score": 85, 
        "match_level": "High / Medium / Low",
        "executive_summary": "A detailed 4-5 sentence paragraph analyzing the fit. Be specific about years of experience, domain knowledge, and major red flags.",
        "strengths": ["List 3-4 major strengths found in the resume"],
        "missing_skills": ["List 4-5 specific technical or soft skills MISSING from the resume that are in the JD"],
        "recommendations": [
            {{
                "title": "Recommendation 1 Title",
                "description": "A comprehensive 3-sentence paragraph explaining exactly HOW to fix this and WHY it matters."
            }},
            {{
                "title": "Recommendation 2 Title",
                "description": "Detailed advice..."
            }}
        ]
    }}
    """
    response_text = ask_ai(prompt)
    try:
        cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_text)
    except:
        return None

# 5. SIDEBAR
with st.sidebar:
    st.title("⚡ JobFit Pro")
    st.markdown("### 1. Upload Resumes")
    # CHANGED: accept_multiple_files=True
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
    
    st.markdown("### 2. Job Description")
    job_desc = st.text_area("Paste text here", height=250, label_visibility="collapsed", placeholder="Paste JD here...")
    
    st.markdown("---")
    st.caption(f"Files Uploaded: {len(uploaded_files) if uploaded_files else 0}")
    st.caption("Powered by Gemini 2.5")

# 6. MAIN CONTENT
st.title("Get things done with your career.")
st.markdown("Batch processing enabled: Analyze multiple candidates at once.")
st.markdown("<br>", unsafe_allow_html=True)

# 7. FEATURES
t1, t2, t3, t4, t5 = st.tabs([
    "📊 Batch Analysis", 
    "✨ Resume Enhancer", 
    "🔗 LinkedIn Optimizer", 
    "✍️ Cover Letter", 
    "🎤 Interview"
])

# --- TAB 1: BATCH ANALYSIS ---
with t1:
    st.header("Candidate Leaderboard")
    
    if st.button("Analyze All Resumes", key="btn1"):
        if uploaded_files and job_desc:
            results = []
            progress_bar = st.progress(0)
            
            for i, file in enumerate(uploaded_files):
                text = extract_text(file)
                if text:
                    data = analyze_single_resume(text, job_desc)
                    if data:
                        data['filename'] = file.name
                        results.append(data)
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            # Sort results by score (Highest first)
            results.sort(key=lambda x: x['match_score'], reverse=True)
            
            if results:
                # 1. SHOW TOP CANDIDATE
                top = results[0]
                st.markdown(f"""
                    <div class="score-container">
                        <div class="score-title">🏆 Top Candidate: {top['filename']}</div>
                        <div class="score-value">{top['match_score']}%</div>
                        <div class="score-sub">{top['match_level']} Match</div>
                    </div>
                """, unsafe_allow_html=True)

                # 2. SHOW LEADERBOARD & DETAILS
                for res in results:
                    with st.expander(f"📄 {res['filename']} — Score: {res['match_score']}%"):
                        st.markdown(f"**Executive Summary:** {res['executive_summary']}")
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            st.write("✅ **Strengths:**")
                            for s in res['strengths']: st.markdown(f"- {s}")
                        with c2:
                            st.write("⚠️ **Missing Skills:**")
                            for s in res['missing_skills']: st.markdown(f"- {s}")
                        
                        st.markdown("---")
                        st.write("💡 **Recommendations:**")
                        for rec in res['recommendations']:
                            st.info(f"**{rec['title']}:** {rec['description']}")
            else:
                st.error("Could not analyze resumes. Please check files.")
        else:
            st.warning("Please upload at least one resume and a job description.")

# HELPER: Select Box with UNIQUE KEY
def get_selected_file(key_suffix):
    if not uploaded_files:
        return None
    names = [f.name for f in uploaded_files]
    # FIX: Added unique key parameter
    selected_name = st.selectbox("Select Resume to Process:", names, key=f"sel_{key_suffix}")
    # Find the actual file object
    return next(f for f in uploaded_files if f.name == selected_name)

# --- TAB 2: RESUME ENHANCER ---
with t2:
    st.header("Resume Content Enhancer")
    target_file = get_selected_file("enhancer")
    
    if st.button("Enhance Selected Resume", key="btn2"):
        if target_file and job_desc:
            with st.spinner("Rewriting..."):
                text = extract_text(target_file)
                if text:
                    prompt = f"""
                    Act as an Expert Resume Writer.
                    1. Identify the 3 weakest bullet points in this resume relative to the JD.
                    2. Rewrite them into "Power Bullets" using the STAR method.
                    3. Write a new, high-impact Professional Summary.
                    RESUME: {text}
                    JD: {job_desc}
                    """
                    st.markdown(ask_ai(prompt))
        else:
            st.warning("Upload resumes and select one.")

# --- TAB 3: LINKEDIN OPTIMIZER ---
with t3:
    st.header("LinkedIn Optimizer")
    target_file = get_selected_file("linkedin")
    
    if st.button("Optimize Profile", key="btn3"):
        if target_file and job_desc:
            with st.spinner("Optimizing..."):
                text = extract_text(target_file)
                if text:
                    prompt = f"""
                    Create a LinkedIn optimization plan.
                    1. 3 Viral Headlines.
                    2. About Section (150 words).
                    3. Top Skills to pin.
                    RESUME: {text}
                    JD: {job_desc}
                    """
                    st.markdown(ask_ai(prompt))

# --- TAB 4: COVER LETTER ---
with t4:
    st.header("Instant Cover Letter")
    target_file = get_selected_file("cover")
    
    if st.button("Draft Letter", key="btn4"):
        if target_file and job_desc:
            with st.spinner("Writing..."):
                text = extract_text(target_file)
                if text:
                    prompt = f"Write a professional cover letter. RESUME: {text} JD: {job_desc}"
                    st.markdown(ask_ai(prompt))

# --- TAB 5: INTERVIEW PREP ---
with t5:
    st.header("Mock Interview")
    target_file = get_selected_file("interview")
    
    if st.button("Generate Question", key="btn5"):
        if target_file and job_desc:
            with st.spinner("Thinking..."):
                text = extract_text(target_file)
                if text:
                    prompt = f"Generate 1 very difficult interview question & STAR answer. RESUME: {text} JD: {job_desc}"
                    st.markdown(ask_ai(prompt))
