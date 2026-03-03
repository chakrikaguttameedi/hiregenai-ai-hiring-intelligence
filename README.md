# 🏢 HireGenAI — AI Hiring Intelligence Platform

A sophisticated multi-agent recruitment pipeline built with **LangGraph**, **Google Gemini 2.5 Flash**, and **Streamlit**. **HireGenAI** automates talent acquisition by parsing resumes, analyzing job descriptions, and generating personalized interview strategies.

---

## 🚀 Features

- 📄 **Resume Parser** — Extracts structured data (Skills, Experience, Education) from PDF/TXT files.
- 🎯 **JD Analyzer** — Breaks down job descriptions into required skills and minimum experience.
- ⚖️ **Hybrid Scorer** — Ranks candidates using a weighted formula: $60\%$ Skills + $30\%$ Experience + $10\%$ Education.
- 💡 **AI Insights** — Generates 3 concise bullet points explaining why a candidate stands out.
- 💬 **Interview Architect** — Crafts 5 tailored technical questions based on the candidate's background.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io/) | Web UI & Dashboard |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Multi-agent state machine orchestration |
| [Google Gemini 2.5 Flash](https://ai.google.dev/) | LLM powering extraction and reasoning |
| [Pydantic](https://docs.pydantic.dev/) | Structured data validation |
| [PyPDF2](https://pypdf2.readthedocs.io/) | PDF text extraction engine |

---

## 🧠 Agent Pipeline

The system uses a sequential **StateGraph** to ensure data flows accurately:

[Resume & JD Input]
│
▼
[Resume Parser Node] ──► Structured JSON Data
│
▼
[JD Analyzer Node]   ──► Extraction of Requirements
│
▼
[Matching Agent]     ──► Calculates Match & Missing Skills
│
▼
[Interview Agent]    ──► Generates 5 Custom Questions


---

## 📁 Project Structure

HireGenAI/
│
├── app.py               # Main application & LangGraph logic
├── requirements.txt     # Python dependencies
└── outputs/             # Application screenshots
├── 1.jpeg

├── 2.jpeg

└── 3.jpeg


---

## 📸 Outputs

### 1. Dashboard & File Upload
<img src="outputs/1.jpeg" alt="Dashboard" width="800"/>

### 2. Candidate Ranking & Insights
<img src="outputs/2.jpeg" alt="Ranking" width="800"/>

### 3. Interview Plan & Summary
<img src="outputs/3.jpeg" alt="Interview Plan" width="800"/>

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).