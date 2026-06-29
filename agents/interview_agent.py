import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_interview_questions(resume_text, job_description):
    prompt = f"""
Based on this resume and job description, generate 8 likely interview questions:
- 4 technical/role-specific questions
- 2 behavioral questions
- 2 questions specifically probing weak/missing areas in the resume vs job description

Resume:
{resume_text}

Job Description:
{job_description}

Just list the 8 questions, numbered, grouped under "Technical", "Behavioral", "Probing Gaps".
"""
    response = model.generate_content(prompt)
    return response.text


def evaluate_answer(question, user_answer, job_description):
    prompt = f"""
You are an interview coach.

Question asked: {question}
Candidate's answer: {user_answer}
Job context: {job_description}

Give brutally honest feedback in under 80 words:
- What was good
- What was missing or weak
- One specific way to improve the answer
"""
    response = model.generate_content(prompt)
    return response.text