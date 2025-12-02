import PyPDF2
import json
import re

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def clean_and_parse_json(response_text):
    # Remove markdown code blocks (```json ... ```)
    text = response_text.replace('```json', '').replace('```', '').strip()
    
    # Attempt to find the first '{' and last '}' to isolate JSON
    start = text.find('{')
    end = text.rfind('}') + 1
    
    if start != -1 and end != 0:
        json_str = text[start:end]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None