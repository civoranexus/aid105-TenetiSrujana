from src.models.deadline_risk_engine import analyze_deadline_risk


def generate_recommendation_report(result):
    score = result["score"]
    confidence = result["confidence"]
    scheme = result["scheme"]
    reasons = result["reasons"]
    scheme_data = result["scheme_data"]

    deadline_risk = analyze_deadline_risk(scheme_data)

    if deadline_risk["urgency"] == "EXPIRED":
        priority = "CLOSED"
    elif score >= 80:
        priority = "APPLY IMMEDIATELY"
    elif score >= 50:
        priority = "PREPARE DOCUMENTS"
    else:
        priority = "NOT RECOMMENDED"

    documents = ["Aadhaar Card", "Income Certificate", "Residence Proof"]

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
        "estimated_loss": deadline_risk.get("estimated_loss", "Low risk"),
        "required_documents": documents
    }
