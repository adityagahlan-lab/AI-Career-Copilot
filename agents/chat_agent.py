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

Rules:
- Keep every reply under 80 words unless the user explicitly asks for a detailed explanation.
- Maximum 80 words.
- Maximum 5 bullet points.
- Be brutally honest.
- Be slightly sarcastic.
- Don't waste words.
- Never write essays.
- Get straight to the point.
- End with one actionable recommendation.
"""

    response = model.generate_content(prompt)

    return response.text