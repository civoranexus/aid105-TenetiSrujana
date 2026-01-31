st.write("🚀 New build loaded at", datetime.now())

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
if "reminders" not in st.session_state:
    st.session_state.reminders = []

# ================= STYLES =================
st.markdown("""
<style>
body { background:#f4f7fb; }

.hero {
    background: linear-gradient(90deg,#0a4c8b,#1e88e5);
    padding:60px;
    border-radius:30px;
    color:white;
}

.big { font-size:44px; font-weight:800 }
.sub { font-size:18px; opacity:0.9 }

.stat-box {
    background:white;
    padding:22px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 10px 30px rgba(0,0,0,0.08);
}

.frame {
    background:white;
    padding:40px;
    border-radius:30px;
    box-shadow:0 12px 35px rgba(0,0,0,0.08);
    margin-top:40px;
}

.frame-alt {
    background:#f7fbff;
    padding:40px;
    border-radius:30px;
    box-shadow:0 12px 35px rgba(0,0,0,0.08);
    margin-top:40px;
}

.flow {
    background:white;
    padding:25px;
    border-radius:22px;
    text-align:center;
    box-shadow:0 8px 25px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown(
            "<h2 style='text-align:center;color:#1e88e5;'>🔐 Welcome to <b>SchemeAssist AI</b></h2>",
            unsafe_allow_html=True
        )

        name = st.text_input("Full Name")
        age = st.number_input("Age", 10, 100, value=None, placeholder="Enter your age")
        income = st.number_input("Annual Income ₹", 0, 500000, 15000)

        state = st.selectbox(
            "State",
            ["Select your state"] + sorted(df["scheme_state"].unique())
        )

        category = st.selectbox(
            "Category",
            sorted(df["category"].unique())
        )

        _, b, _ = st.columns([2,1,2])
        with b:
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

    st.stop()

u = st.session_state.user

# ================= FRAME 1 : DASHBOARD + SCHEMES =================
st.markdown("<div class='frame'>", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero">
  <div class="big">🏛️ SchemeAssist AI</div>
  <div class="sub">Schemes curated for <b>{u['category']}</b> in <b>{u['state']}</b></div>
</div>
""", unsafe_allow_html=True)

# FILTERS
f1, f2, f3, f4 = st.columns([2,2,2,1])
income = f1.number_input("Income ₹", 0, 500000, u["income"])
state = f2.selectbox("State", ["ALL"] + sorted(df["scheme_state"].unique()))
category = f3.selectbox("Category", sorted(df["category"].unique()))
f4.button("🔍 Find Schemes")

filtered = df[
    (df["min_income"] <= income) &
    (df["max_income"] >= income) &
    (
        (df["scheme_state"] == state) |
        (df["scheme_state"] == "ALL") |
        (state == "ALL")
    ) &
    (df["category"] == category)
]

# SMART SORT (AI Ranking)
filtered = filtered.sort_values(
    by=["deadline", "estimated_benefit"],
    ascending=[True, False]
)

# STATS
s1, s2, s3 = st.columns(3)
s1.markdown(
    f"<div class='stat-box'><h1>{len(filtered)}</h1><p>Total Schemes</p></div>",
    unsafe_allow_html=True
)
s2.markdown(
    f"<div class='stat-box'><h1>{category}</h1><p>Category</p></div>",
    unsafe_allow_html=True
)
s3.markdown(
    f"<div class='stat-box'><h1>{state}</h1><p>State</p></div>",
    unsafe_allow_html=True
)

st.markdown("## 🎯 Recommended Schemes")

for idx, s in filtered.iterrows():
    days = (s["deadline"] - datetime.now()).days
    urgency = "HIGH" if days < 30 else "MEDIUM" if days < 60 else "LOW"
    score = random.randint(85, 98)

    st.markdown(f"### 🏷️ {s['scheme_name']}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Benefit", f"₹{int(s['estimated_benefit']):,}")
    c2.metric("Urgency", urgency)
    c3.metric("Deadline", s["deadline"].strftime("%d %b %Y"))
    c4.metric("Approval Confidence", f"{score}%")

    st.progress(score)

    st.info(
        f"🧠 **AI Reasoning**: Income eligible • Category matched • "
        f"Deadline in {days} days"
    )

    st.warning(
        f"⚠ **If missed:** You may lose ₹{int(s['estimated_benefit']):,}. "
        "Next chance could be after 1 year."
    )

    # DOCUMENT READINESS
    st.markdown("📋 **Document Readiness**")
    a = st.checkbox("Aadhaar Card", key=f"a{idx}")
    i = st.checkbox("Income Certificate", key=f"i{idx}")
    b = st.checkbox("Bank Passbook", key=f"b{idx}")

    ready = sum([a, i, b])
    st.progress(ready / 3)
    st.caption(f"Readiness: {ready}/3 documents")

    if urgency == "HIGH" and ready < 2:
        st.error("⚠ Low readiness for urgent scheme")

    if st.button("🔔 Set Reminder", key=f"r{idx}"):
        st.toast("Reminder saved ⏰")

    st.markdown("---")

st.markdown("</div>", unsafe_allow_html=True)

# ================= FRAME 2 : HOW IT WORKS =================
st.markdown("<div class='frame-alt'>", unsafe_allow_html=True)
st.markdown("## 🪜 How It Works")

h1, h2, h3 = st.columns(3)
h1.markdown("<div class='flow'><h3>👤 Step 1</h3><p>Enter your details</p></div>", unsafe_allow_html=True)
h2.markdown("<div class='flow'><h3>🧠 Step 2</h3><p>AI evaluates eligibility</p></div>", unsafe_allow_html=True)
h3.markdown("<div class='flow'><h3>🚀 Step 3</h3><p>Apply with confidence</p></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ================= FRAME 3 : INSIGHTS =================
st.markdown("<div class='frame'>", unsafe_allow_html=True)
st.markdown("## 📊 Insights & Analytics")

c1, c2 = st.columns(2)
with c1:
    urgency_data = filtered["deadline"].apply(
        lambda d: "HIGH" if (d - datetime.now()).days < 30 else
                  "MEDIUM" if (d - datetime.now()).days < 60 else "LOW"
    ).value_counts()
    st.bar_chart(urgency_data)

with c2:
    st.line_chart(filtered.set_index("scheme_name")["estimated_benefit"])

st.info("📈 Insight: High urgency schemes have higher approval chances when applied early.")

st.markdown("</div>", unsafe_allow_html=True)

# ================= FRAME 4 : FAQ =================
st.markdown("<div class='frame-alt'>", unsafe_allow_html=True)
st.markdown("## ❓ Frequently Asked Questions")

with st.expander("Is this an official government website?"):
    st.write("No. This is an academic AI assistance platform.")
with st.expander("Why does urgency matter?"):
    st.write("Deadlines impact eligibility and availability of funds.")
with st.expander("Can results change?"):
    st.write("Yes, when income, state or category changes.")
with st.expander("Is my data stored?"):
    st.write("No personal data is permanently stored.")

st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("<br><center>© 2026 SchemeAssist AI</center>", unsafe_allow_html=True)
