import streamlit as st
import google.generativeai as genai
import os
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
    # Using the working model
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.stop()

# 3. SUPERLIST DESIGN (Dark & Red)
st.markdown("""
    <style>
    /* IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* GLOBAL COLORS */
    .stApp {
        background-color: #0E0E10; /* Deep Charcoal */
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #FFFFFF;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #18181B; 
        border-right: 1px solid #27272A;
    }

    /* ACCENT COLOR (Superlist Red) */
    a { color: #FF5B45 !important; }
    
    /* BUTTONS (Pill Shape & Red) */
    .stButton > button {
        background-color: #FF5B45 !important;
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.8;
    }

    /* HEADERS */
    h1, h2, h3 {
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        color: #FFFFFF !important;
    }

    /* CARDS */
    div[data-testid="stExpander"] {
        background-color: #18181B;
        border-radius: 12px;
        border: 1px solid #27272A;
    }
    
    /* INPUTS */
    .stTextInput input, .stTextArea textarea {
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

# 5. SIDEBAR
with st.sidebar:
    st.title("⚡ JobFit Pro")
    st.markdown("### 1. Upload Resume")
    uploaded_file = st.file_uploader("PDF Only", type="pdf", label_visibility="collapsed")
    
    st.markdown("### 2. Job Description")
    job_desc = st.text_area("Paste text here", height=250, label_visibility="collapsed", placeholder="Paste JD here...")
    
    st.markdown("---")
    st.caption("Powered by Gemini 2.5")

# 6. MAIN CONTENT
st.title("Get things done with your career.")
st.markdown("AI-powered optimization for every step of your application.")
st.markdown("<br>", unsafe_allow_html=True)

# 7. ALL FEATURES (Tabs)
t1, t2, t3, t4, t5 = st.tabs([
    "📊 Match Analysis", 
    "✨ Resume Enhancer", 
    "🔗 LinkedIn Optimizer", 
    "✍️ Cover Letter", 
    "🎤 Interview"
])

# --- TAB 1: MATCH ANALYSIS ---
with t1:
    st.header("Resume Match Report")
    if st.button("Analyze Match", key="btn1"):
        if uploaded_file and job_desc:
            with st.spinner("Analyzing..."):
                text = extract_text(uploaded_file)
                if text:
                    prompt = f"""
                    Act as a Senior Recruiter. Compare Resume to JD.
                    RESUME: {text}
                    JD: {job_desc}
                    Output Markdown:
                    1. **Match Score** (Big Number)
                    2. **✅ Matching Skills**
                    3. **⚠️ Missing Keywords**
                    4. **💡 3 Fixes**
                    """
                    st.markdown(ask_ai(prompt))
        else:
            st.warning("Upload Resume & JD first.")

# --- TAB 2: RESUME ENHANCER (Restored) ---
with t2:
    st.header("Resume Content Enhancer")
    st.write("Rewrite your bullet points to be punchy and impact-driven.")
    if st.button("Enhance Resume", key="btn2"):
        if uploaded_file and job_desc:
            with st.spinner("Rewriting..."):
                text = extract_text(uploaded_file)
                if text:
                    prompt = f"""
                    Act as a Resume Writer. 
                    1. Rewrite the top 3 weak bullet points from this resume using the STAR method to fit the JD.
                    2. Write a new 3-sentence Professional Summary.
                    RESUME: {text}
                    JD: {job_desc}
                    """
                    st.markdown(ask_ai(prompt))
        else:
            st.warning("Upload Resume & JD first.")

# --- TAB 3: LINKEDIN OPTIMIZER (Restored) ---
with t3:
    st.header("LinkedIn Profile Optimizer")
    st.write("Get a headline and bio that attracts recruiters.")
    if st.button("Optimize Profile", key="btn3"):
        if uploaded_file and job_desc:
            with st.spinner("Optimizing..."):
                text = extract_text(uploaded_file)
                if text:
                    prompt = f"""
                    Create a LinkedIn profile based on this resume/JD.
                    1. 3 Catchy Headlines.
                    2. A 'About' section (150 words, storytelling).
                    3. List of Skills to add to the Skills Section.
                    RESUME: {text}
                    JD: {job_desc}
                    """
                    st.markdown(ask_ai(prompt))
        else:
            st.warning("Upload Resume & JD first.")

# --- TAB 4: COVER LETTER ---
with t4:
    st.header("Instant Cover Letter")
    if st.button("Draft Letter", key="btn4"):
        if uploaded_file and job_desc:
            with st.spinner("Writing..."):
                text = extract_text(uploaded_file)
                if text:
                    prompt = f"Write a professional cover letter. RESUME: {text} JD: {job_desc}"
                    st.markdown(ask_ai(prompt))
        else:
            st.warning("Upload Resume & JD first.")

# --- TAB 5: INTERVIEW PREP ---
with t5:
    st.header("Mock Interview")
    if st.button("Generate Question", key="btn5"):
        if uploaded_file and job_desc:
            with st.spinner("Thinking..."):
                text = extract_text(uploaded_file)
                if text:
                    prompt = f"Generate 1 hard interview question & STAR answer. RESUME: {text} JD: {job_desc}"
                    st.markdown(ask_ai(prompt))
        else:
            st.warning("Upload Resume & JD first.")
