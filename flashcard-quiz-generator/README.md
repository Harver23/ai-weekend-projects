# 🧠 Flashcard & Quiz Generator

Paste your notes in, get auto-generated flashcards and quiz questions out.
A genuinely useful study tool — the kind you'll actually keep using after you build it.

Runs entirely on your own machine through [Ollama](https://ollama.com), so there's
no API key and no per-request cost.

## How it works

1. You paste raw notes into a text box.
2. The app sends them to a local LLM (via Ollama) with a prompt asking for JSON back.
3. Streamlit renders the flashcards as expandable cards and the quiz as an
   interactive multiple-choice test with instant feedback.

## Setup

1. **Install Ollama** — https://ollama.com/download
2. **Pull a model:**
   ```bash
   ollama pull llama3.2
   ```
3. **Start Ollama** (if it isn't already running as a service):
   ```bash
   ollama serve
   ```
4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Notes

- If Ollama runs on a different host/port, edit `OLLAMA_URL` in `app.py`.
- Swap `MODEL` for any model you've pulled (e.g. `mistral`, `phi3`) — smaller models
  are faster but may produce less reliable JSON.
- The prompt asks for strict JSON; if a model ever returns malformed JSON, just
  regenerate — this is a known quirk of smaller local models.
