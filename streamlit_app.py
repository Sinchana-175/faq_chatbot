import streamlit as st
import requests
from prompt_template import build_prompt

# Remember last subject
if "last_subject" not in st.session_state:
    st.session_state.last_subject = "ds"


def load_syllabus(subject):
    try:
        with open(f"syllabus/{subject}.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Syllabus not found."


def detect_subject(question):
    q = question.lower().strip()

    if any(word in q for word in ["data structure", "ds", "stack", "queue", "tree", "graph", "array"]):
        st.session_state.last_subject = "ds"

    elif any(word in q for word in ["dbms", "database", "sql", "normalization"]):
        st.session_state.last_subject = "dbms"

    elif any(word in q for word in ["os", "operating system", "process", "thread", "cpu scheduling", "memory"]):
        st.session_state.last_subject = "os"

    elif any(word in q for word in [
        "machine learning", "ml",
        "regression", "classification", "clustering",
        "probability", "distribution", "model"
    ]):
        st.session_state.last_subject = "ml"

    elif any(word in q for word in ["ai", "artificial intelligence", "ir"]):
        return "unknown"

    return st.session_state.last_subject


def ask_question(question):
    subject = detect_subject(question)

    if subject == "unknown":
        return "This subject is not available in the syllabus."

    syllabus = load_syllabus(subject)

    prompt = build_prompt(question, syllabus)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()


# ---------------- UI ---------------- #

st.set_page_config(page_title="FAQ Chatbot", layout="centered")

st.title("Smart FAQ Chatbot")

user_input = st.text_input("Ask your question:")

if st.button("Get Answer"):
    if user_input:
        with st.spinner("Thinking..."):
            answer = ask_question(user_input)

        st.subheader("Answer:")
        st.write(answer)
    else:
        st.warning("Please enter a question")