def compare_top_schemes(ranked_schemes, reports_map):
    """
    Compare top 2 schemes and explain which one should be applied first
    """

    if len(ranked_schemes) < 2:
        return None

    first = ranked_schemes[0]
    second = ranked_schemes[1]

    r1 = reports_map[first["scheme"]]
    r2 = reports_map[second["scheme"]]

    reasons = []

    # Urgency comparison
    if r1["urgency"] != r2["urgency"]:
        reasons.append(
            f"Higher urgency ({r1['urgency']}) compared to {r2['urgency']}"
        )

    # Benefit comparison
    if first["estimated_benefit"] > second["estimated_benefit"]:
        reasons.append(
            f"Higher financial benefit (₹{first['estimated_benefit']})"
        )

    # Readiness comparison
    if len(r1["required_documents"]) < len(r2["required_documents"]):
        reasons.append("Requires fewer documents to apply")

    # Fallback
    if not reasons:
        reasons.append("Better overall AI ranking score")

    return {
        "apply_first": first["scheme"],
        "apply_later": second["scheme"],
        "reasons": reasons
    }
