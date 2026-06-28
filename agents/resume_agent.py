import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an expert career coach and ATS resume reviewer.

Resume:
{resume_text}

Job Description:
{job_description}

Analyze the resume and provide:

1. Resume Summary
2. Strengths
3. Weaknesses
4. Missing Skills
5. ATS Match Score out of 100
6. Suggestions to Improve

Give the answer in clean markdown.
"""

    response = model.generate_content(prompt)
    return response.text