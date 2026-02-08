def explain_rejection(scheme_result):
    reasons = []

    if scheme_result["score"] < 50:
        reasons.append("Eligibility score is below the safe threshold.")

    if "Income does not meet eligibility criteria" in scheme_result["reasons"]:
        reasons.append("Declared income does not satisfy scheme requirements.")

    if scheme_result.get("confidence") == "LOW":
        reasons.append("Low confidence due to multiple unmet conditions.")

    if not reasons:
        reasons.append("Scheme is deprioritized based on AI risk assessment.")

    return reasons
