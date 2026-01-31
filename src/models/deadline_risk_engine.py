def analyze_deadline_risk(scheme_data):
    deadline = scheme_data.get("deadline")

    if not deadline:
        return {
            "status": "OPEN",
            "urgency": "LOW",
            "risk_level": "LOW",
            "warning": "✅ Sufficient time available",
            "estimated_loss": "Low risk"
        }

    if isinstance(deadline, str) and deadline.lower() == "expired":
        return {
            "status": "EXPIRED",
            "urgency": "EXPIRED",
            "risk_level": "CRITICAL",
            "warning": "❌ Deadline missed. Scheme no longer available.",
            "estimated_loss": "No action possible (scheme closed)"
        }

    return {
        "status": "OPEN",
        "urgency": "LOW",
        "risk_level": "LOW",
        "warning": "✅ Sufficient time available",
        "estimated_loss": "Low risk"
    }
