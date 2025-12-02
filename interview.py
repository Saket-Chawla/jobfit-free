from utils import clean_and_parse_json

def get_interview_tips(model, resume_text, job_desc):
    prompt = f"""
    Generate interview prep. Return ONLY JSON:
    {{
        "preparation_tips": ["Tip 1", "Tip 2"],
        "questions_to_expect": ["Technical Question 1", "Technical Question 2"],
        "behavioral_questions": ["Behavioral Question 1", "Behavioral Question 2"]
    }}
    JD: {job_desc}
    Resume: {resume_text}
    """
    response = model.generate_content(prompt)
    return clean_and_parse_json(response.text)