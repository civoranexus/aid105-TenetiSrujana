def generate_decision_trace(result):
    scheme = result["scheme"]
    score = result["score"]
    confidence = result["confidence"]
    reasons = result["reasons"]
    scheme_data = result["scheme_data"]

    trace = []

    trace.append(
        f"Eligibility score {score} computed using income, state, and category rules."
    )

    if any("urgency" in r.lower() for r in reasons):
        trace.append(
            "Deadline urgency significantly increased recommendation priority."
        )

    benefit = int(scheme_data.get("estimated_benefit", 0))
    if benefit >= 50000:
        trace.append(
            f"High financial impact (₹{benefit}) strengthened the recommendation."
        )
    else:
        trace.append(
            f"Moderate financial impact (₹{benefit}) resulted in a balanced recommendation."
        )

    trace.append(
        f"Final confidence level set to {confidence} after combining all factors."
    )

    return trace
