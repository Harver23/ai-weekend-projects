# 💸 Personal Finance Categorizer

Upload a bank statement, and it sorts every spend into a category and flags
anything unusual. A small, real demonstration of applying AI to messy,
personal data — exactly the kind of thing companies want to see you can do.

## How it works

- **Categorization** is keyword-based: each transaction description is matched
  against a category dictionary (groceries, dining, transport, etc.). Simple,
  transparent, and easy to extend — no training data needed.
- **Anomaly detection** uses scikit-learn's `IsolationForest`, run separately
  within each category, to flag transactions whose amount looks out of place
  compared to your usual spending in that category (e.g. a ₹45,000 "Shopping"
  charge among mostly ₹1,000–3,000 ones).

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then upload a CSV, or try `sample_statement.csv` (included) to see it work
immediately.

## CSV format expected

| date       | description        | amount |
|------------|---------------------|--------|
| 2026-06-01 | BIGBASKET GROCERY    | 1450   |

- `amount` should be positive for spends. Income (e.g. salary) can be negative
  or given the "Salary/Income" keyword — it's excluded from anomaly checks by
  category rules, not amount sign, so keep descriptions clear.

## Extending it

- Add more keywords to `CATEGORY_KEYWORDS` in `app.py` for categories specific
  to your own spending (subscriptions, gym, etc.).
- Swap the keyword matcher for a trained text classifier once you have enough
  labeled data — the categorization function is a single, isolated function,
  so it's a drop-in replacement.
