import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def get_ats_score(resume_text, job_description):
    prompt = f"""
You are an ATS (Applicant Tracking System) simulator.

Resume:
{resume_text}

Job Description:
{job_description}

Task:
1. Give an ATS match score out of 100.
2. List the top 5 missing keywords/skills from the job description not found in the resume.
3. List 3 formatting/structure issues that could hurt ATS parsing (e.g. tables, headers, fonts — infer from text structure only).
4. Give 3 quick fixes to improve the score.

Format your response with clear headers: Score, Missing Keywords, Formatting Issues, Quick Fixes.
Keep it concise — no more than 150 words total.
"""
    response = model.generate_content(prompt)
    return response.text