# 🚀 HireGenAI — AI Hiring Intelligence Platform

HireGenAI is an AI-powered resume evaluation and candidate intelligence platform designed to automate and enhance the hiring process using Large Language Models (LLMs).

It intelligently analyzes uploaded resumes against a given job description, ranks candidates based on skill alignment, detects potential bias, generates professional hiring insights, and creates an interview question plan — all in one streamlined system.

---

## 🌟 Key Features

- 📄 Upload Multiple Resumes (PDF Format)
- 🧠 AI-Based Resume Parsing & Skill Extraction
- 🎯 Smart Job Description Matching
- 🏆 Automated Candidate Ranking
- 📊 Matched & Missing Skills Analysis
- 💡 Professional Candidate Impression Summary
- ⚖️ Bias Detection & Candidate Comparison Insights
- 📈 Selection Percentage Display
- 📝 Interview Questions Plan (Generated On-Demand)
- 🌙 Dark-Themed Professional UI
- ☁️ Streamlit Cloud Deployment Ready

---

## 🧠 How the System Works

1. Upload one or more resumes (PDF format).
2. Provide the job description.
3. The system extracts skills and experience from resumes.
4. It compares them against job requirements using an LLM.
5. Generates:
   - Ranked candidate list
   - Skill gap analysis
   - Professional hiring justification
   - Selection percentage
   - Interview question plan (via button)
6. Displays a final hiring recommendation.

---

## 🛠️ Tech Stack

- **Frontend & UI:** Streamlit
- **LLM:** Gemini 2.5 Flash
- **Framework:** LangGraph
- **LLM Integration:** LangChain
- **PDF Processing:** PyPDF2
- **Environment Handling:** python-dotenv
- **Deployment:** Streamlit Cloud

---

## 📂 Project Structure

hiregenai-ai-hiring-intelligence/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── outputs/
    ├── 1.jpeg
    ├── 2.jpeg
    └── 3.jpeg

---

## ⚙️ Local Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/hiregenai-ai-hiring-intelligence.git
cd hiregenai-ai-hiring-intelligence