from datetime import datetime

def analyze_deadline_risk(scheme_data):
    deadline_str = scheme_data.get("deadline")

    today = datetime.now().date()
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()

    days_left = (deadline - today).days

    if days_left < 0:
        return {
            "status": "EXPIRED",
            "urgency": "EXPIRED",
            "risk_level": "CRITICAL",
            "warning": "❌ Deadline missed. Scheme no longer available.",
            "estimated_loss": "No action possible (scheme closed)"
        }

    if days_left <= 7:
        return {
            "status": "ACTIVE",
            "urgency": "EXTREME",
            "risk_level": "VERY HIGH",
            "warning": f"⚠️ Only {days_left} days left to apply!",
            "estimated_loss": f"₹{scheme_data['estimated_benefit']} potential benefit at risk"
        }

    return {
        "status": "ACTIVE",
        "urgency": "LOW",
        "risk_level": "LOW",
        "warning": "✅ Sufficient time available",
        "estimated_loss": "Low financial risk"
    }
