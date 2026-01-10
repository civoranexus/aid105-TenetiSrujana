from models.deadline_risk_engine import analyze_deadline_risk

def generate_recommendation_report(scheme_result):
    score = scheme_result["score"]
    confidence = scheme_result["confidence"]
    scheme = scheme_result["scheme"]
    reasons = scheme_result["reasons"]
    scheme_data = scheme_result["scheme_data"]

    deadline_risk = analyze_deadline_risk(scheme_data)

    if score >= 80 or deadline_risk["urgency"] in ["EXTREME"]:
        priority = "APPLY IMMEDIATELY"
    elif score >= 50:
        priority = "PREPARE DOCUMENTS"
    else:
        priority = "NOT RECOMMENDED CURRENTLY"

    documents = ["Aadhaar Card", "Income Certificate", "Residence Proof"]

    if "Scholarship" in scheme:
        documents.append("Bonafide / Study Certificate")

    if "Housing" in scheme:
        documents.append("Land Ownership / Ration Card")

    steps = [
        f"Review eligibility criteria for {scheme}",
        "Collect required documents",
        "Apply via official government portal",
        "Track application status regularly"
    ]

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
        "required_documents": documents,
        "next_steps": steps
    }
