import streamlit as st

def setup_style():
    st.markdown("""
        <style>
        /* 1. LOAD FONT (Poppins for a Tech Look) */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #f8f9fc;
        }

        /* 2. GRADIENT HERO CARD */
        .hero-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 20px rgba(118, 75, 162, 0.3);
            margin-bottom: 30px;
            animation: fadeIn 0.8s;
        }
        .hero-card h1 {
            font-size: 80px;
            margin: 0;
            font-weight: 700;
            color: white !important;
            text-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .hero-card p {
            font-size: 18px;
            opacity: 0.9;
            margin-top: 5px;
            color: #e0e7ff !important;
        }

        /* 3. MODERN METRIC CARDS */
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            text-align: center;
            border: 1px solid #f0f0f0;
            transition: transform 0.2s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            border-color: #764ba2;
        }
        .stat-val {
            font-size: 32px;
            font-weight: 700;
            color: #2d3748;
        }
        .stat-label {
            color: #718096;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }

        /* 4. SKILL TAGS */
        .skill-tag {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 500;
            margin: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .skill-yes { background-color: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }
        .skill-no { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }

        /* 5. COMPARISON CARDS (Before/After) */
        .compare-box {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 5px solid #cbd5e0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .compare-box.good { border-left-color: #48bb78; }
        .compare-box.bad { border-left-color: #f56565; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

def display_analysis(analysis):
    if not analysis: return

    # 1. THE HERO SECTION (HTML Gradient Card)
    st.markdown(f"""
        <div class="hero-card">
            <h1>{analysis['overall_match']}%</h1>
            <p>JOB MATCH SCORE</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. METRICS ROW (HTML Cards)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Technical Skills</div>
                <div class="stat-val" style="color:#4299e1;">{analysis['categories']['technical_skills']['match']}%</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Soft Skills</div>
                <div class="stat-val" style="color:#ed8936;">{analysis['categories']['soft_skills']['match']}%</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Experience</div>
                <div class="stat-val" style="color:#48bb78;">{analysis['categories']['experience']['match']}%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. DETAILED SKILLS
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Present Skills")
        for s in analysis['categories']['technical_skills']['present_skills']:
            st.markdown(f'<span class="skill-tag skill-yes">✓ {s}</span>', unsafe_allow_html=True)
            
    with col2:
        st.subheader("⚠️ Missing Skills")
        for s in analysis['categories']['technical_skills']['missing_skills']:
            st.markdown(f'<span class="skill-tag skill-no">✕ {s}</span>', unsafe_allow_html=True)

def display_enhancement(data):
    if not data: return
    
    st.markdown("### 🚀 Professional Summary Upgrade")
    st.info(data['summary_section']['sample_summary'])
    
    st.markdown("### 💎 Bullet Point Transformation")
    for w, s in zip(data['bullet_points']['weak_bullets'], data['bullet_points']['improved_versions']):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="compare-box bad"><b>❌ ORIGINAL:</b><br>{w}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="compare-box good"><b>✅ IMPROVED:</b><br>{s}</div>', unsafe_allow_html=True)

def display_linkedin(data):
    if not data: return
    st.subheader("✨ Headlines")
    for h in data['headline_suggestions']:
        st.markdown(f"- **{h}**")
    st.subheader("📝 About Section")
    st.code(data['about_section'], language='text')

def display_interview(data):
    if not data: return
    st.info(f"💡 **Pro Tip:** {data['preparation_tips'][0]}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🔥 Technical Questions")
        for q in data['questions_to_expect']:
            st.markdown(f"- {q}")
    with c2:
        st.subheader("🧠 Behavioral Questions")
        for q in data['behavioral_questions']:
            st.markdown(f"- {q}")