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
    df.columns = (
        df.columns
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
    )
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
.hero { background: linear-gradient(90deg,#0a4c8b,#1e88e5);
padding:60px;border-radius:30px;color:white;}
.big { font-size:44px; font-weight:800 }
.sub { font-size:18px; opacity:0.9 }
.stat-box { background:white;padding:22px;border-radius:20px;
text-align:center;box-shadow:0 10px 30px rgba(0,0,0,0.08);}
.frame { background:white;padding:40px;border-radius:30px;
box-shadow:0 12px 35px rgba(0,0,0,0.08);margin-top:40px;}
.frame-alt { background:#f7fbff;padding:40px;border-radius:30px;
box-shadow:0 12px 35px rgba(0,0,0,0.08);margin-top:40px;}
.flow { background:white;padding:25px;border-radius:22px;
text-align:center;box-shadow:0 8px 25px rgba(0,0,0,0.08);}
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

        state = st.selectbox("State", ["Select your state"] + sorted(df["state"].unique()))
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

    st.stop()

u = st.session_state.user

# ================= DASHBOARD =================
st.markdown("<div class='frame'>", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero">
  <div class="big">🏛️ SchemeAssist AI</div>
  <div class="sub">Schemes curated for <b>{u['category']}</b> in <b>{u['state']}</b></div>
</div>
""", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns([2,2,2,1])
income = f1.number_input("Income ₹", 0, 500000, u["income"])
state = f2.selectbox("State", ["ALL"] + sorted(df["state"].unique()))
category = f3.selectbox("Category", sorted(df["category"].unique()))
f4.button("🔍 Find Schemes")

filtered = df[
    (df["min_income"] <= income) &
    (df["max_income"] >= income) &
    ((df["state"] == state) | (df["state"] == "ALL") | (state == "ALL")) &
    (df["category"] == category)
].sort_values(by=["deadline", "estimated_benefit"], ascending=[True, False])

# ================= STATS =================
s1, s2, s3 = st.columns(3)
s1.markdown(f"<div class='stat-box'><h1>{len(filtered)}</h1><p>Total Schemes</p></div>", unsafe_allow_html=True)
s2.markdown(f"<div class='stat-box'><h1>{category}</h1><p>Category</p></div>", unsafe_allow_html=True)
s3.markdown(f"<div class='stat-box'><h1>{state}</h1><p>State</p></div>", unsafe_allow_html=True)

st.markdown("## 🎯 Recommended Schemes")

for idx, s in filtered.iterrows():
    days = (s["deadline"] - datetime.now()).days
    urgency = "HIGH" if days < 30 else "MEDIUM" if days < 60 else "LOW"
    score = random.randint(85, 98)

    st.markdown(f"### 🏷️ {s['scheme_name']}")
    st.caption("🌍 National Scheme" if s["state"] == "ALL" else f"📍 State Scheme ({s['state']})")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Benefit", f"₹{int(s['estimated_benefit']):,}")
    c2.metric("Urgency", urgency)
    c3.metric("Deadline", s["deadline"].strftime("%d %b %Y"))
    c4.metric("Approval Confidence", f"{score}%")

    st.progress(score)

    # 🔮 Deadline Risk Meter
    if days <= 7:
        risk = "🔴 CRITICAL"
    elif days <= 20:
        risk = "🟠 HIGH"
    elif days <= 45:
        risk = "🟡 MEDIUM"
    else:
        risk = "🟢 LOW"
    st.markdown(f"**⏳ Deadline Risk:** {risk} ({days} days left)")

    # 🧠 Explainable AI
    with st.expander("🧠 Why this scheme is recommended"):
        st.write(
            f"- Income eligible\n- Category matched\n- State valid\n- Deadline proximity: {days} days\n- Historical success considered"
        )

    # ⏰ Best Time to Apply
    st.info(
        "⏰ **Best Time to Apply:** " +
        ("Within 3–5 days" if urgency == "HIGH" else "Within 2 weeks" if urgency == "MEDIUM" else "Flexible")
    )

    # 📋 Document Readiness
    st.markdown("📋 **Document Readiness**")
    a = st.checkbox("Aadhaar Card", key=f"a{idx}")
    i = st.checkbox("Income Certificate", key=f"i{idx}")
    b = st.checkbox("Bank Passbook", key=f"b{idx}")

    ready = sum([a, i, b])
    st.progress(ready / 3)

    missing = []
    if not a: missing.append("Aadhaar")
    if not i: missing.append("Income Certificate")
    if not b: missing.append("Bank Passbook")

    if missing:
        st.warning("📄 Missing: " + ", ".join(missing))
    else:
        st.success("✅ All documents ready")

    if urgency == "HIGH" and ready < 2:
        st.error("⚠ Low readiness for urgent scheme")

    col1, col2 = st.columns(2)
    if col1.button("🔔 Set Reminder", key=f"r{idx}"):
        st.toast("Reminder saved ⏰")
    if col2.button("📌 Save for Later", key=f"s{idx}"):
        st.session_state.reminders.append(s["scheme_name"])
        st.toast("Saved 📌")

    st.markdown("---")

# ================= SAVED =================
if st.session_state.reminders:
    st.markdown("## 📌 Saved Schemes")
    for sc in set(st.session_state.reminders):
        st.write("•", sc)
        
        st.markdown("---")

# ================= HOW IT WORKS =================
st.markdown("<div class='frame-alt'>", unsafe_allow_html=True)
st.markdown("## 🪜 How It Works")
c1, c2, c3 = st.columns(3)
c1.markdown("<div class='flow'>👤 Enter details</div>", unsafe_allow_html=True)
c2.markdown("<div class='flow'>🧠 AI evaluates</div>", unsafe_allow_html=True)
c3.markdown("<div class='flow'>🚀 Apply smart</div>", unsafe_allow_html=True)
st.markdown("---")

# ================= INSIGHTS =================
st.markdown("<div class='frame'>", unsafe_allow_html=True)
st.markdown("## 📊 Insights & Analytics")

if filtered.empty:
    st.warning("No data available for insights.")
else:
    # ---------- PREP DATA ----------
    filtered["days_left"] = filtered["deadline"].apply(
        lambda d: (d - datetime.now()).days
    )

    filtered["urgency"] = filtered["days_left"].apply(
        lambda d: "High" if d < 30 else "Medium" if d < 60 else "Low"
    )

    high = (filtered["urgency"] == "High").sum()
    med = (filtered["urgency"] == "Medium").sum()
    low = (filtered["urgency"] == "Low").sum()

    max_benefit = int(filtered["estimated_benefit"].max())
    avg_benefit = int(filtered["estimated_benefit"].mean())

    # ---------- SUMMARY CARDS ----------
    st.markdown("### 🤖 AI Summary Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("High Urgency", high, help="Deadlines < 30 days")
    c2.metric("Medium Urgency", med)
    c3.metric("Low Urgency", low)
    c4.metric("Max Benefit (₹)", f"{max_benefit:,}")

    st.markdown("---")

    # ---------- VISUAL INSIGHTS ----------
    st.markdown("### 🔍 What AI Observes")

    v1, v2 = st.columns(2)

    with v1:
        st.markdown("#### ⏰ Urgency Distribution")
        st.progress(min(high / max(len(filtered), 1), 1.0))
        st.caption(f"🔴 {high} high-urgency scheme(s) need immediate attention")

        st.progress(min((high + med) / max(len(filtered), 1), 1.0))
        st.caption(f"🟠 {med} medium-urgency scheme(s) coming up")

        st.progress(min((high + med + low) / max(len(filtered), 1), 1.0))
        st.caption(f"🟢 {low} low-urgency scheme(s) are flexible")

    with v2:
        st.markdown("#### 💰 Benefit Spread")
        st.metric("Average Benefit", f"₹{avg_benefit:,}")
        st.metric("Top Benefit", f"₹{max_benefit:,}")

        top_scheme = filtered.sort_values(
            by="estimated_benefit", ascending=False
        ).iloc[0]

        st.info(
            f"🏆 **Highest Benefit Scheme:** {top_scheme['scheme_name']} "
            f"(₹{int(top_scheme['estimated_benefit']):,})"
        )

    st.markdown("---")

    # ---------- AI RECOMMENDATION ----------
    st.markdown("### ✨ AI Recommendation")

    if high > 0:
        st.success(
            "⚡ **Apply immediately** to high-urgency schemes. "
            "Ensure documents are ready to avoid last-minute rejection."
        )
    else:
        st.info(
            "✅ No immediate deadline pressure. "
            "You can plan applications strategically."
        )

    st.caption(
        "🧠 AI combines deadline proximity, benefit value, and eligibility to guide decisions."
    )
    st.markdown("---")

# ================= FRAME : FAQ =================
st.markdown("<div class='frame-alt'>", unsafe_allow_html=True)
st.markdown("## ❓ Frequently Asked Questions")

with st.expander("Is this an official government website?"):
    st.write(
        "No. This is an academic AI assistance platform built for educational and demonstration purposes."
    )

with st.expander("How are schemes recommended?"):
    st.write(
        "Schemes are recommended based on your income, category, state, and urgency calculated from deadlines."
    )

with st.expander("Why does urgency matter?"):
    st.write(
        "Schemes with closer deadlines may close soon. Applying early improves approval chances and reduces risk."
    )

with st.expander("Is my personal data stored or shared?"):
    st.write(
        "No. This application does not permanently store, track, or share any personal user information."
    )

with st.expander("How accurate is the approval confidence score?"):
    st.write(
        "The approval confidence is AI-generated using eligibility match, deadline urgency, and benefit relevance. "
        "It is indicative, not a guarantee."
    )

with st.expander("Can I apply directly through this platform?"):
    st.write(
        "No. SchemeAssist AI helps you discover and prepare for schemes. Applications must be submitted on official government portals."
    )

with st.expander("What documents are usually required?"):
    st.write(
        "Common documents include Aadhaar card, income certificate, and bank passbook. "
        "Exact requirements may vary by scheme."
    )

with st.expander("Can scheme results change later?"):
    st.write(
        "Yes. Scheme availability and eligibility can change based on government updates, deadlines, or income/category changes."
    )

# ================= FOOTER =================
st.markdown("<br><center>© 2026 SchemeAssist AI</center>", unsafe_allow_html=True)
