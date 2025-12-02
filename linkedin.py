from utils import clean_and_parse_json

def get_linkedin_optimization(model, resume_text):
    prompt = f"""
    Analyze resume for LinkedIn. Return ONLY JSON:
    {{
        "headline_suggestions": ["Catchy Headline 1", "Catchy Headline 2", "Headline 3"],
        "about_section": "Write a storytelling-style LinkedIn 'About' section (approx 100 words).",
        "skills_to_add": ["List 5 top skills for LinkedIn Skills section"],
        "profile_optimization": ["Tip 1 for visibility", "Tip 2 for networking"]
    }}
    Resume: {resume_text}
    """
    response = model.generate_content(prompt)
    return clean_and_parse_json(response.text)