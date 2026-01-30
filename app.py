import streamlit as st
import pandas as pd
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="SchemeAssist AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("src/data/schemes_master.csv")
    df["deadline"] = pd.to_datetime(df["deadline"])
    return df

df = load_data()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= STYLES =================
st.markdown("""
<style>
body { background:#f4f7fb; }

/* HERO */
.hero {
    background: linear-gradient(90deg,#0a4c8b,#1e88e5);
    padding:60px;
    border-radius:30px;
    color:white;
}
.big { font-size:44px; font-weight:800 }
.sub { font-size:18px; opacity:0.9 }

/* STATS */
.stat-box {
    background:white;
    padding:22px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 10px 30px rgba(0,0,0,0.08);
}

/* TABS */
.stTabs [data-baseweb="tab"] {
    font-size:18px !important;
    font-weight:600 !important;
    padding:14px 26px !important;
    border-radius:20px !important;
    background:#eef3fb !important;
    margin-right:12px !important;
}
.stTabs [aria-selected="true"] {
    background:#1e88e5 !important;
    color:white !important;
}

/* SECTION BORDER */
.section {
    background:white;
    padding:40px;
    border-radius:28px;
    border:3px solid #1e88e5;
    box-shadow:0 18px 45px rgba(0,0,0,0.12);
    margin:40px 0;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("""
        <div class="section">
            <h2>🔐 Welcome to <b>SchemeAssist AI</b></h2>
        """, unsafe_allow_html=True)

        name = st.text_input("Full Name")
        age = st.number_input("Age", 10, 100, 20)
        income = st.number_input("Annual Income ₹", 0, 500000, 15000)
        state = st.selectbox("State", ["ALL"] + sorted(df["scheme_state"].unique()))
        category = st.selectbox("Category", sorted(df["category"].unique()))

        if st.button("🚀 Enter Dashboard"):
            st.session_state.user = {
                "name": name,
                "age": age,
                "income": income,
                "state": state,
                "category": category
            }
            st.session_state.logged_in = True
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

u = st.session_state.user

# ================= HERO =================
st.markdown(f"""
<div class="hero">
  <div class="big">🏛️ SchemeAssist AI</div>
  <div class="sub">Smart Government Scheme Discovery for {u['name']}</div>
</div>
""", unsafe_allow_html=True)

# ================= FILTER =================
f1,f2,f3,f4 = st.columns([2,2,2,1])
income = f1.number_input("Income ₹",0,500000,u["income"])
state = f2.selectbox("State",["ALL"]+sorted(df["scheme_state"].unique()))
category = f3.selectbox("Category",sorted(df["category"].unique()))
f4.button("🔍 Find Schemes")

filtered = df[
    (df["min_income"] <= income) &
    (df["max_income"] >= income) &
    ((df["scheme_state"] == state) | (df["scheme_state"]=="ALL") | (state=="ALL")) &
    (df["category"] == category)
]

# ================= STATS =================
s1,s2,s3 = st.columns(3)
s1.markdown(f"<div class='stat-box'><h1>{len(filtered)}</h1><p>Total Schemes</p></div>", unsafe_allow_html=True)
s2.markdown(f"<div class='stat-box'><h1>{category}</h1><p>Category</p></div>", unsafe_allow_html=True)
s3.markdown(f"<div class='stat-box'><h1>{state}</h1><p>State</p></div>", unsafe_allow_html=True)

# ================= RECOMMENDED SCHEMES =================
st.markdown("""
<div class="section">
    <h2>🎯 Recommended Schemes</h2>
""", unsafe_allow_html=True)

for idx, s in filtered.iterrows():
    days = (s["deadline"] - datetime.now()).days
    urgency = "HIGH" if days < 30 else "MEDIUM" if days < 60 else "LOW"

    st.markdown(f"### 🏷️ {s['scheme_name']}")

    c1,c2,c3 = st.columns(3)
    c1.metric("Benefit", f"₹{int(s['estimated_benefit']):,}")
    c2.metric("Urgency", urgency)
    c3.metric("Deadline", s["deadline"].strftime("%d %b %Y"))

    tabs = st.tabs(["🧠 AI Decision","👤 Explanation","📋 Readiness","📅 Action Plan"])

    with tabs[0]:
        st.write("✔ Income & category verified")
        st.write("✔ State eligibility matched")
        st.write("✔ Deadline urgency considered")
        st.progress(80 if urgency=="HIGH" else 60)

    with tabs[1]:
        st.info("You are eligible. Apply before deadline.")

    with tabs[2]:
        st.checkbox("Income Certificate", key=f"inc_{idx}")
        st.checkbox("Residence Proof", key=f"res_{idx}")

    with tabs[3]:
        st.button("🔔 Set Reminder", key=f"rem_{idx}")

    st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("<br><center>© 2026 SchemeAssist AI</center>", unsafe_allow_html=True)
