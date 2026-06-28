import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from agents.resume_agent import analyze_resume

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Career Assistant")

st.write("Upload your resume and paste the job description.")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if st.button("Analyze"):

    if uploaded_file is None:
        st.error("Please upload a resume.")

    elif job_description.strip() == "":
        st.error("Please paste a job description.")

    else:
        resume_text = extract_text_from_pdf(uploaded_file)

        with st.spinner("🤖 AI is analyzing your resume..."):
            result = analyze_resume(resume_text, job_description)

        st.success("Analysis Complete!")

        st.markdown(result)