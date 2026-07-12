"""Personal Finance Categorizer — upload a bank statement CSV,
get spends auto-categorized and unusual transactions flagged.
"""
import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest

CATEGORY_KEYWORDS = {
    "Groceries": ["grocery", "supermarket", "mart", "bigbasket", "grofers"],
    "Dining": ["restaurant", "cafe", "coffee", "swiggy", "zomato", "starbucks"],
    "Transport": ["uber", "ola", "fuel", "petrol", "metro", "irctc"],
    "Shopping": ["amazon", "flipkart", "myntra", "mall"],
    "Bills & Utilities": ["electricity", "recharge", "broadband", "gas", "water"],
    "Entertainment": ["netflix", "spotify", "prime video", "bookmyshow"],
    "Rent": ["rent"],
    "Health": ["pharmacy", "hospital", "clinic", "apollo"],
    "Salary/Income": ["salary", "credited", "refund"],
}


def categorize(description: str) -> str:
    text = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(k in text for k in keywords):
            return category
    return "Other"


def flag_unusual(df: pd.DataFrame) -> pd.Series:
    """Flag unusual transactions using IsolationForest on amount (per category)."""
    flags = pd.Series(False, index=df.index)
    for category, group in df.groupby("category"):
        if len(group) < 4:  # too few points for a meaningful model
            continue
        model = IsolationForest(contamination="auto", random_state=42)
        preds = model.fit_predict(group[["amount"]])
        flags.loc[group.index] = preds == -1
    return flags


st.set_page_config(page_title="Personal Finance Categorizer", page_icon="💸")
st.title("💸 Personal Finance Categorizer")
st.caption("Upload a bank statement CSV. Spends get sorted into categories, and unusual ones get flagged.")

st.info(
    "CSV needs columns: **date**, **description**, **amount** "
    "(amount should be positive for spends).",
    icon="ℹ️",
)

uploaded = st.file_uploader("Upload bank statement CSV", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
    missing = {"date", "description", "amount"} - set(df.columns.str.lower())
    if missing:
        st.error(f"CSV is missing columns: {', '.join(missing)}")
    else:
        df.columns = df.columns.str.lower()
        df["category"] = df["description"].apply(categorize)
        df["unusual"] = flag_unusual(df)

        st.subheader("Spend by category")
        st.bar_chart(df.groupby("category")["amount"].sum())

        st.subheader("🚩 Unusual transactions")
        unusual_df = df[df["unusual"]]
        if unusual_df.empty:
            st.write("Nothing unusual flagged — spends look consistent.")
        else:
            st.dataframe(unusual_df[["date", "description", "amount", "category"]])

        st.subheader("All transactions")
        st.dataframe(df[["date", "description", "amount", "category", "unusual"]])

        st.download_button(
            "Download categorized CSV",
            df.to_csv(index=False),
            file_name="categorized_transactions.csv",
        )
