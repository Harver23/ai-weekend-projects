# Weekend Projects

Two small projects — each buildable and usable in a weekend.

| Project | What it does | Stack |
|---|---|---|
| [`flashcard-quiz-generator/`](./flashcard-quiz-generator) | Paste notes, get flashcards + a quiz | Ollama (local LLM) + Streamlit |
| [`finance-categorizer/`](./finance-categorizer) | Upload a bank statement, get spends categorized and unusual ones flagged | pandas + scikit-learn + Streamlit |

Each folder is a standalone app with its own `README.md` and
`requirements.txt` — go into either folder and follow its setup steps.

## Why these two

- **Flashcard & Quiz Generator** — a study tool you'll actually keep using,
  and it costs nothing to run since the model runs locally.
- **Personal Finance Categorizer** — shows AI applied to real, messy personal
  data (a bank statement), which is closer to what most AI jobs actually look
  like than a toy dataset.

## Repo layout

```
ai-weekend-projects/
├── flashcard-quiz-generator/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── finance-categorizer/
│   ├── app.py
│   ├── requirements.txt
│   ├── sample_statement.csv
│   └── README.md
└── README.md   (this file)
```
