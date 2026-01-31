import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="SchemeAssist AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("src/data/schemes_master.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.lower()
    df["deadline"] = pd.to_datetime(df["deadline"])
    return df

df = load_data()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN =================
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center'>🔐 Welcome to SchemeAssist AI</h2>", unsafe_allow_html=True)

    name = st.text_input("Full Name")
    age = st.number_input("Age", 10, 100)
    income = st.number_input("Annual Income ₹", 0, 500000, 15000)

    category = st.selectbox(
        "Category",
        sorted(df["category"].unique())
    )

    if st.button("🚀 Enter Dashboard"):
        st.session_state.user = {
            "name": name,
            "age": age,
            "income": income,
            "category": category
        }
        st.session_state.logged_in = True
        st.rerun()

    st.stop()

u = st.session_state.user

# ================= FILTER =================
filtered = df[
    (df["min_income"] <= u["income"]) &
    (df["max_income"] >= u["income"]) &
    (df["category"] == u["category"])
]

filtered = filtered.sort_values(
    by=["deadline", "estimated_benefit"],
    ascending=[True, False]
)

# ================= DASHBOARD =================
st.markdown(f"## 🎯 Schemes for category: {u['category']}")

for _, s in filtered.iterrows():
    days = (s["deadline"] - datetime.now()).days
    score = random.randint(85, 98)

    st.subheader(s["scheme_name"])
    st.write(f"💰 Benefit: ₹{int(s['estimated_benefit']):,}")
    st.write(f"📅 Deadline: {s['deadline'].date()}")
    st.progress(score)
    st.markdown("---")

st.markdown("<center>© 2026 SchemeAssist AI</center>", unsafe_allow_html=True)
