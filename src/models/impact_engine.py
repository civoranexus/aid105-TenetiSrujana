def generate_impact_summary(report):
    score = report["score"]
    urgency = report["urgency"]
    estimated_loss = report["estimated_loss"]
    scheme = report["scheme"]

    if "₹" in estimated_loss:
        financial_impact = estimated_loss
    else:
        financial_impact = "Minimal financial impact"

    if urgency in ["EXTREME", "HIGH"]:
        outcome = "Immediate action required to avoid loss"
    elif score >= 60:
        outcome = "Action recommended but not urgent"
    else:
        outcome = "Low impact — can be skipped safely"

    return {
        "scheme": scheme,
        "financial_impact": financial_impact,
        "outcome": outcome
    }
