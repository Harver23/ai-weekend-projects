"""Flashcard & Quiz Generator — paste notes, get flashcards + quiz questions.
Uses a local Ollama model, so it's free and runs offline.
"""
import json
import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

PROMPT_TEMPLATE = """You are a study assistant. From the notes below, generate:
- 5 flashcards (front/back)
- 3 multiple-choice quiz questions (question, 4 options, correct_answer)

Return ONLY valid JSON, no extra text, in this exact shape:
{{
  "flashcards": [{{"front": "...", "back": "..."}}],
  "quiz": [{{"question": "...", "options": ["...", "...", "...", "..."], "correct_answer": "..."}}]
}}

Notes:
{notes}
"""


def generate_study_set(notes: str) -> dict:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": PROMPT_TEMPLATE.format(notes=notes),
            "stream": False,
            "format": "json",
        },
        timeout=120,
    )
    response.raise_for_status()
    return json.loads(response.json()["response"])


st.set_page_config(page_title="Flashcard & Quiz Generator", page_icon="🧠")
st.title("🧠 Flashcard & Quiz Generator")
st.caption("Paste your notes. Get flashcards and a quiz. Runs on your machine via Ollama — no API cost.")

notes = st.text_area("Paste your notes here", height=220, placeholder="Paste lecture notes, textbook summary, etc.")

if st.button("Generate study set", type="primary", disabled=not notes.strip()):
    with st.spinner("Thinking..."):
        try:
            result = generate_study_set(notes)
            st.session_state["result"] = result
        except requests.exceptions.ConnectionError:
            st.error("Can't reach Ollama. Run `ollama serve` and make sure the model is pulled (see README).")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if "result" in st.session_state:
    result = st.session_state["result"]

    st.subheader("📇 Flashcards")
    for i, card in enumerate(result.get("flashcards", []), 1):
        with st.expander(f"Card {i}: {card['front']}"):
            st.write(card["back"])

    st.subheader("📝 Quiz")
    for i, q in enumerate(result.get("quiz", []), 1):
        st.write(f"**Q{i}. {q['question']}**")
        choice = st.radio("Choose one:", q["options"], key=f"q{i}", index=None, label_visibility="collapsed")
        if choice is not None:
            if choice == q["correct_answer"]:
                st.success("Correct!")
            else:
                st.error(f"Not quite — correct answer: {q['correct_answer']}")
