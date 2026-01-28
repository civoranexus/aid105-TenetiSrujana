from models.deadline_risk_engine import analyze_deadline_risk


def generate_recommendation_report(scheme_result):
    score = scheme_result["score"]
    confidence = scheme_result["confidence"]
    scheme = scheme_result["scheme"]
    reasons = scheme_result["reasons"]
    scheme_data = scheme_result["scheme_data"]

    # Deadline risk analysis
    deadline_risk = analyze_deadline_risk(scheme_data)

    # 🚨 HARD OVERRIDE FOR EXPIRED SCHEMES
    if deadline_risk["status"] == "EXPIRED":
        priority = "CLOSED"
    elif score >= 80 or deadline_risk["urgency"] == "EXTREME":
        priority = "APPLY IMMEDIATELY"
    elif score >= 50:
        priority = "PREPARE DOCUMENTS"
    else:
        priority = "NOT RECOMMENDED CURRENTLY"

    # Required documents
    documents = [
        "Aadhaar Card",
        "Income Certificate",
        "Residence Proof"
    ]

    if "Scholarship" in scheme:
        documents.append("Bonafide / Study Certificate")

    if "Housing" in scheme:
        documents.append("Land Ownership / Ration Card")

    return {
        "scheme": scheme,
        "priority": priority,
        "confidence": confidence,
        "score": score,
        "reasons": reasons,
        "urgency": deadline_risk["urgency"],
        "risk_level": deadline_risk["risk_level"],
        "warning": deadline_risk["warning"],
        "estimated_loss": deadline_risk["estimated_loss"],
        "required_documents": documents
    }
