def compare_schemes(schemes):
    """
    Compare multiple schemes and explain why one ranks higher than another.
    """

    comparisons = []

    for i in range(len(schemes) - 1):
        better = schemes[i]
        lower = schemes[i + 1]

        reasons = []

        if better["rank_score"] > lower["rank_score"]:
            reasons.append("higher overall AI rank score")

        comparisons.append({
            "better_scheme": better["scheme"],
            "lower_scheme": lower["scheme"],
            "reasons": reasons
        })

    return comparisons
