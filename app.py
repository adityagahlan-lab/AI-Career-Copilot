import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from agents.resume_agent import analyze_resume
from agents.chat_agent import chat_with_ai
from agents.ats_agent import get_ats_score
from agents.cover_letter_agent import generate_cover_letter
from agents.interview_agent import generate_interview_questions, evaluate_answer
from agents.roadmap_agent import generate_roadmap

st.set_page_config(page_title="AI Career Copilot", page_icon="🤖", layout="wide")
st.title("🤖 AI Career Copilot")

# ---------- SETUP (shared across all tabs) ----------
st.write("Upload your resume and paste the job description once — all tools below use it.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if uploaded_file and job_description.strip():
    st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
    st.session_state.job_description = job_description
    st.success("Resume and job description loaded — use any tool below.")

ready = "resume_text" in st.session_state and "job_description" in st.session_state

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Resume Analyzer", "🎯 ATS Score", "✍️ Cover Letter",
    "🎤 Interview Prep", "🗺️ Roadmap", "💬 Career Chat"
])

# ---------- TAB 1: RESUME ANALYZER ----------
with tab1:
    if not ready:
        st.info("Upload resume + job description above first.")
    else:
        if st.button("Analyze Resume", key="analyze_btn"):
            with st.spinner("Analyzing..."):
                result = analyze_resume(st.session_state.resume_text, st.session_state.job_description)
                st.session_state.analysis = result
            st.markdown(result)
        elif "analysis" in st.session_state:
            st.markdown(st.session_state.analysis)

# ---------- TAB 2: ATS SCORE ----------
with tab2:
    if not ready:
        st.info("Upload resume + job description above first.")
    else:
        if st.button("Check ATS Score"):
            with st.spinner("Scanning like an ATS bot..."):
                result = get_ats_score(st.session_state.resume_text, st.session_state.job_description)
            st.markdown(result)

# ---------- TAB 3: COVER LETTER ----------
with tab3:
    if not ready:
        st.info("Upload resume + job description above first.")
    else:
        tone = st.selectbox("Tone", ["professional", "enthusiastic", "concise", "confident"])
        if st.button("Generate Cover Letter"):
            with st.spinner("Writing..."):
                result = generate_cover_letter(st.session_state.resume_text, st.session_state.job_description, tone)
            st.markdown(result)

# ---------- TAB 4: INTERVIEW PREP ----------
with tab4:
    if not ready:
        st.info("Upload resume + job description above first.")
    else:
        if st.button("Generate Interview Questions"):
            with st.spinner("Preparing questions..."):
                st.session_state.interview_questions = generate_interview_questions(
                    st.session_state.resume_text, st.session_state.job_description
                )

        if "interview_questions" in st.session_state:
            st.markdown(st.session_state.interview_questions)
            st.divider()
            st.subheader("Practice an Answer")
            q = st.text_input("Paste a question from above")
            a = st.text_area("Your answer")
            if st.button("Get Feedback"):
                with st.spinner("Evaluating..."):
                    feedback = evaluate_answer(q, a, st.session_state.job_description)
                st.markdown(feedback)

# ---------- TAB 5: ROADMAP ----------
with tab5:
    if not ready:
        st.info("Upload resume + job description above first.")
    else:
        if st.button("Generate Roadmap"):
            with st.spinner("Mapping your path..."):
                result = generate_roadmap(st.session_state.resume_text, st.session_state.job_description)
            st.markdown(result)

# ---------- TAB 6: CAREER CHAT ----------
with tab6:
    if not ready:
        st.info("Upload resume + job description above first.")
    elif "analysis" not in st.session_state:
        st.info("Run 'Resume Analyzer' tab first so the chat has context.")
    else:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask your question...")

        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.spinner("Thinking..."):
                reply = chat_with_ai(
                    question,
                    st.session_state.resume_text,
                    st.session_state.job_description,
                    st.session_state.analysis,
                    st.session_state.messages
                )

            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)