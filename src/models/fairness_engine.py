def audit_fairness(reports):
    """
    Evaluates whether any citizen category is unfairly favored or ignored.
    """

    category_scores = {}
    category_counts = {}

    for r in reports:
        category = r.get("category", "UNKNOWN")
        score = r.get("score", 0)

        category_scores.setdefault(category, 0)
        category_counts.setdefault(category, 0)

        category_scores[category] += score
        category_counts[category] += 1

    insights = []

    for category in category_scores:
        avg_score = category_scores[category] / category_counts[category]

        if avg_score >= 75:
            insights.append(
                f"✔ {category} category receives strong AI support (avg score {avg_score:.1f})"
            )
        elif avg_score >= 50:
            insights.append(
                f"ℹ {category} category receives moderate AI consideration (avg score {avg_score:.1f})"
            )
        else:
            insights.append(
                f"⚠ {category} category may be under-supported (avg score {avg_score:.1f})"
            )

    return insights
