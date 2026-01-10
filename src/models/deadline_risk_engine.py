from datetime import datetime

def analyze_deadline_risk(scheme):
    today = datetime.today().date()
    deadline = datetime.strptime(scheme["deadline"], "%Y-%m-%d").date()

    days_left = (deadline - today).days

    if days_left <= 0:
        urgency = "EXPIRED"
        warning = "❌ Deadline missed. Scheme no longer available."
        risk_level = "CRITICAL"

    elif days_left <= 7:
        urgency = "EXTREME"
        warning = f"⚠️ Only {days_left} days left to apply!"
        risk_level = "VERY HIGH"

    elif days_left <= 15:
        urgency = "HIGH"
        warning = f"⏳ Deadline approaching in {days_left} days"
        risk_level = "HIGH"

    elif days_left <= 30:
        urgency = "MEDIUM"
        warning = f"🕒 {days_left} days remaining"
        risk_level = "MODERATE"

    else:
        urgency = "LOW"
        warning = "✅ Sufficient time available"
        risk_level = "LOW"

    estimated_loss = (
        f"₹{scheme['estimated_benefit']} potential benefit at risk"
        if urgency in ["EXTREME", "HIGH"]
        else "Low financial risk"
    )

    return {
        "days_left": days_left,
        "urgency": urgency,
        "risk_level": risk_level,
        "warning": warning,
        "estimated_loss": estimated_loss
    }
