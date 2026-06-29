import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_roadmap(resume_text, job_description):
    prompt = f"""
Compare this resume against the job description and create a skill-gap learning roadmap.

Resume:
{resume_text}

Job Description:
{job_description}

Output format:
1. Skill Gaps (bullet list, max 5, ordered by importance)
2. 30/60/90-day roadmap — what to learn/build in each phase to close the gaps
3. One project idea per major gap that would demonstrate the skill

Keep it concise and actionable, under 200 words.
"""
    response = model.generate_content(prompt)
    return response.text