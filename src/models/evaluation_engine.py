def evaluate_ranking(ranked_schemes):
    """
    Explains WHY schemes are ranked in a particular order
    using rank_score, priority weight, and benefit impact.
    """

    explanations = []

    for i in range(len(ranked_schemes) - 1):
        current = ranked_schemes[i]
        next_one = ranked_schemes[i + 1]

        reasons = []

        if current["rank_score"] > next_one["rank_score"]:
            reasons.append("higher overall AI rank score")

        if current.get("estimated_benefit", 0) > next_one.get("estimated_benefit", 0):
            reasons.append("greater estimated financial benefit")

        if current.get("priority_weight", 0) > next_one.get("priority_weight", 0):
            reasons.append("higher policy priority weight")

        explanations.append({
            "better_scheme": current["scheme"],
            "lower_scheme": next_one["scheme"],
            "reasons": reasons or ["stronger combined AI factors"]
        })

    return explanations
