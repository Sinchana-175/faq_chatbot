import requests
from prompt_template import build_prompt

# Remember last subject
last_subject = "ds"


def load_syllabus(subject):
    try:
        with open(f"syllabus/{subject}.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Syllabus not found."


def detect_subject(question):
    global last_subject
    q = question.lower().strip()

    # Data Structures
    if any(word in q for word in [
        "data structure", "ds", "stack", "queue",
        "tree", "graph", "array"
    ]):
        last_subject = "ds"

    # DBMS
    elif any(word in q for word in [
        "dbms", "database", "sql", "normalization"
    ]):
        last_subject = "dbms"

    # Operating Systems
    elif any(word in q for word in [
        "os", "operating system", "process",
        "thread", "cpu scheduling", "memory"
    ]):
        last_subject = "os"

    # Machine Learning
    elif any(word in q for word in [
        "machine learning", "ml",
        "regression", "classification", "clustering",
        "model", "training", "dataset",
        "probability", "distribution", "bayes"
    ]):
        last_subject = "ml"

    # Unknown subjects (AI, IR, etc.)
    elif any(word in q for word in [
        "ai", "artificial intelligence",
        "ir", "information retrieval"
    ]):
        return "unknown"

    return last_subject


def ask_question(question):
    try:
        subject = detect_subject(question)

        # Handle unknown subject
        if subject == "unknown":
            return "This subject is not available in the syllabus. Please ask about DS, DBMS, OS, or ML."

        syllabus = load_syllabus(subject)

        print(f"\nDetected Subject: {subject.upper()}")

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

    except Exception as e:
        return f"Error: {str(e)}"


print("Smart FAQ Chatbot (type 'exit' to quit)\n")

while True:
    user_input = input("Ask your question: ")

    if user_input.lower() == "exit":
        print("Goodbye")
        break

    answer = ask_question(user_input)
    print("\nAnswer:\n", answer, "\n")