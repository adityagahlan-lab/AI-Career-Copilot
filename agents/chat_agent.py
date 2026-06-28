import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def chat_with_ai(question, resume_text, job_description, analysis):

    prompt = f"""
You are an expert AI Career Coach.

You already know the following information:

Resume:
{resume_text}

Job Description:
{job_description}

Previous Resume Analysis:
{analysis}

The user asks:
{question}

Answer naturally and conversationally.
Use the resume and job description as context.
Give practical career advice.
"""

    response = model.generate_content(prompt)

    return response.text