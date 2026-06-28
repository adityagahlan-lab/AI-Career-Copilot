import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from agents.resume_agent import analyze_resume
from agents.chat_agent import chat_with_ai

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

        # Save everything for chat
        st.session_state.resume_text = resume_text
        st.session_state.job_description = job_description
        st.session_state.analysis = result

        st.success("Analysis Complete!")

        st.markdown(result)

# ---------------- AI CHAT ---------------- #

if "analysis" in st.session_state:

    st.divider()
    st.header("💬 Career Coach AI")

    st.write("Ask anything about your resume, interview preparation, projects, roadmap, ATS score, or career.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    question = st.chat_input("Ask your question...")

    if question:

        # Show user's message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # Generate AI response
        with st.spinner("Thinking..."):

            reply = chat_with_ai(
                question,
                st.session_state.resume_text,
                st.session_state.job_description,
                st.session_state.analysis
            )

        # Save AI response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(reply)