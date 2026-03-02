import streamlit as st
import os
from dotenv import load_dotenv
from typing import TypedDict, List
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from PyPDF2 import PdfReader

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="HireGenAI",
    layout="wide"
)

# Dark professional styling
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #f1f5f9;
}
h1, h2, h3, h4 {
    color: #e2e8f0;
}
div[data-testid="stMetricValue"] {
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD API KEY
# -------------------------------------------------
load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    st.error("Please set GOOGLE_API_KEY in .env file")
    st.stop()

# -------------------------------------------------
# LLM INIT
# -------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)

# -------------------------------------------------
# MODELS
# -------------------------------------------------
class ResumeData(BaseModel):
    name: str
    skills: List[str]
    experience_years: float
    education: str


class JDData(BaseModel):
    required_skills: List[str]
    min_experience: float
    role: str


class MatchResult(BaseModel):
    skill_match_score: float
    experience_match_score: float
    overall_score: float
    matched_skills: List[str]
    missing_skills: List[str]


class InterviewQuestions(BaseModel):
    questions: List[str]


# -------------------------------------------------
# STATE
# -------------------------------------------------
class HiringState(TypedDict):
    resume_text: str
    jd_text: str
    resume_data: dict
    jd_data: dict
    match_result: dict
    interview_questions: dict


# -------------------------------------------------
# AGENTS
# -------------------------------------------------
def resume_parser(state: HiringState):
    structured_llm = llm.with_structured_output(ResumeData)
    result = structured_llm.invoke(
        f"Extract structured resume data from:\n{state['resume_text']}"
    )
    return {"resume_data": result.model_dump()}


def jd_analyzer(state: HiringState):
    structured_llm = llm.with_structured_output(JDData)
    result = structured_llm.invoke(
        f"Extract structured job requirements from:\n{state['jd_text']}"
    )
    return {"jd_data": result.model_dump()}


def matching_agent(state: HiringState):
    structured_llm = llm.with_structured_output(MatchResult)
    result = structured_llm.invoke(
        f"""
        Resume Data: {state['resume_data']}
        Job Data: {state['jd_data']}

        Calculate skill match score, experience match score,
        overall score, matched skills and missing skills.
        """
    )
    return {"match_result": result.model_dump()}


def interview_agent(state: HiringState):
    structured_llm = llm.with_structured_output(InterviewQuestions)
    result = structured_llm.invoke(
        f"""
        Based on resume and job description,
        generate 5 personalized technical interview questions.
        Resume: {state['resume_data']}
        Job: {state['jd_data']}
        """
    )
    return {"interview_questions": result.model_dump()}


# -------------------------------------------------
# GRAPH
# -------------------------------------------------
builder = StateGraph(HiringState)

builder.add_node("resume_parser", resume_parser)
builder.add_node("jd_analyzer", jd_analyzer)
builder.add_node("matching_agent", matching_agent)
builder.add_node("interview_agent", interview_agent)

builder.set_entry_point("resume_parser")
builder.add_edge("resume_parser", "jd_analyzer")
builder.add_edge("jd_analyzer", "matching_agent")
builder.add_edge("matching_agent", "interview_agent")
builder.set_finish_point("interview_agent")

app_graph = builder.compile()

# -------------------------------------------------
# HYBRID SCORE
# -------------------------------------------------
def compute_final_score(candidate):
    skill_score = candidate["match_result"]["skill_match_score"]
    exp_score = candidate["match_result"]["experience_match_score"]

    education = candidate["resume_data"]["education"].lower()
    edu_bonus = 10 if "ai" in education or "ml" in education else 0

    final_score = (0.6 * skill_score) + (0.3 * exp_score) + (0.1 * edu_bonus)
    return round(final_score, 2)


# -------------------------------------------------
# FILE TEXT EXTRACTION
# -------------------------------------------------
def extract_text_from_file(file):
    if file.type == "application/pdf":
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text
    else:
        return file.read().decode("utf-8")


# -------------------------------------------------
# UI
# -------------------------------------------------
st.title("🏢✨ HireGenAI — AI Hiring Intelligence Platform")

uploaded_files = st.file_uploader(
    "Upload Resume Files (PDF or TXT)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

jd_text = st.text_area("Job Description", height=200)

if "ranked_candidates" not in st.session_state:
    st.session_state.ranked_candidates = None

# -------------------------------------------------
# EVALUATE BUTTON
# -------------------------------------------------
if st.button("Evaluate Candidates 🚀"):

    if not uploaded_files:
        st.warning("Please upload at least one resume.")
        st.stop()

    results = []

    for file in uploaded_files:
        resume_text = extract_text_from_file(file)

        state = {
            "resume_text": resume_text,
            "jd_text": jd_text,
            "resume_data": {},
            "jd_data": {},
            "match_result": {},
            "interview_questions": {}
        }

        output = app_graph.invoke(state)
        output["final_score"] = compute_final_score(output)
        results.append(output)

    ranked_candidates = sorted(
        results,
        key=lambda x: (
            x["final_score"],
            len(x["match_result"]["matched_skills"]),
            x["resume_data"]["experience_years"]
        ),
        reverse=True
    )

    st.session_state.ranked_candidates = ranked_candidates


# -------------------------------------------------
# DISPLAY RESULTS
# -------------------------------------------------
if st.session_state.ranked_candidates:

    ranked_candidates = st.session_state.ranked_candidates
    top_candidate = ranked_candidates[0]

    st.subheader("🏆 Candidate Ranking Dashboard")

    for i, candidate in enumerate(ranked_candidates, 1):

        name = candidate["resume_data"]["name"]
        score = candidate["final_score"]
        matched = candidate["match_result"]["matched_skills"]
        missing = candidate["match_result"]["missing_skills"]

        st.markdown(f"### 🥇 Rank {i}: {name}" if i == 1 else f"### Rank {i}: {name}")
        st.metric("Selection Match Percentage", f"{score}%")

        st.write("**Matched Skills:**", ", ".join(matched))
        st.write("**Missing Skills:**", ", ".join(missing))

        # AI Strength Summary
        summary = llm.invoke(
            f"Give 3 concise bullet points explaining what is impressive about this candidate for the role.\nCandidate:{candidate}"
        )
        st.write("**Why This Candidate Stands Out:**")
        st.write(summary.content)

        st.markdown("---")

    # -------------------------------------------------
    # SELECTED CANDIDATE
    # -------------------------------------------------
    st.subheader("📌 Selected Candidate Summary")

    st.success(f"{top_candidate['resume_data']['name']} selected with {top_candidate['final_score']}% match")

    abilities_summary = llm.invoke(
        f"Explain in a professional short paragraph why this candidate is ideal for the role.\nCandidate:{top_candidate}"
    )

    st.write(abilities_summary.content)

    # -------------------------------------------------
    # INTERVIEW PLAN
    # -------------------------------------------------
    st.subheader("💬 Interview Questions Plan")

    with st.expander("Click to View AI-Generated Interview Questions"):
        for idx, q in enumerate(top_candidate["interview_questions"]["questions"], 1):
            st.write(f"{idx}. {q}")