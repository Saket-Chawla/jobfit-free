from utils import clean_and_parse_json

def get_resume_enhancement(model, resume_text, job_desc):
    prompt = f"""
    Act as an Expert Resume Writer for Senior Roles. 
    Analyze the resume against the Job Description (JD).
    
    Your goal is to rewrite weak bullet points into "Power Achievements" that are detailed, quantified, and impressive.
    
    Return ONLY valid JSON in this structure:
    {{
        "summary_section": {{ 
            "has_summary": true, 
            "sample_summary": "Write a powerful, 3-4 sentence professional summary tailored to the JD. Focus on years of experience, key specialized skills, and biggest career wins." 
        }},
        "bullet_points": {{ 
            "weak_bullets": [
                "Find the 3 weakest, shortest, or most vague bullet points in the resume."
            ], 
            "improved_versions": [
                "Rewrite each weak bullet into a detailed, heavy-hitting paragraph (2-3 sentences long). MUST use the STAR method (Situation, Task, Action, Result). MUST include specific numbers, percentages, tools used, and business impact. Make it sound like a senior-level achievement."
            ] 
        }},
        "power_verbs": {{ 
            "suggested_verbs": ["List 5 high-impact action verbs (e.g., 'Orchestrated', 'Spearheaded') relevant to this JD"] 
        }}
    }}
    
    JD: {job_desc}
    Resume: {resume_text}
    """
    
    response = model.generate_content(prompt)
    return clean_and_parse_json(response.text)