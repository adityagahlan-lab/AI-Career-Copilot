import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_cover_letter(resume_text, job_description, tone="professional"):
    prompt = f"""
You are an expert cover letter writer.

Resume:
{resume_text}

Job Description:
{job_description}

Write a {tone} cover letter (under 300 words) tailored to this job description, using real details from the resume.
Do not invent experience that isn't in the resume.
Structure: greeting, why this role, 2-3 relevant strengths with specific resume evidence, closing line.
"""
    response = model.generate_content(prompt)
    return response.text