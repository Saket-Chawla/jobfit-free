from utils import clean_and_parse_json

def get_match_analysis(model, job_desc, resume_text):
    prompt = f"""
    Act as an expert ATS scanner. Analyze the JD and Resume.
    Return ONLY valid JSON with this exact structure:
    {{
        "overall_match": <number 0-100>,
        "keyword_match_score": <number 0-100>,
        "categories": {{
            "technical_skills": {{ "match": <number>, "present_skills": [], "missing_skills": [], "improvement_suggestions": [] }},
            "soft_skills": {{ "match": <number>, "present_skills": [], "missing_skills": [] }},
            "experience": {{ "match": <number>, "strengths": [], "gaps": [] }}
        }},
        "ats_optimization": {{ "formatting_issues": [], "keyword_optimization": [] }},
        "impact_scoring": {{ "achievement_metrics": <number>, "action_verbs": <number>, "quantifiable_results": <number>, "improvement_suggestions": [] }}
    }}
    JD: {job_desc}
    Resume: {resume_text}
    """
    response = model.generate_content(prompt)
    return clean_and_parse_json(response.text)