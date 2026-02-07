from datetime import datetime

def rank_schemes(enriched_reports):
    ranked = []

    for report in enriched_reports:
        score = report["score"]
        priority_weight = report["priority_weight"]
        estimated_benefit = report["estimated_benefit"]
        deadline = report["deadline"]

        try:
            days_left = (
                datetime.strptime(deadline, "%Y-%m-%d") - datetime.today()
            ).days
        except Exception:
            days_left = 30

        if days_left <= 7:
            urgency = 1.5
        elif days_left <= 15:
            urgency = 1.2
        else:
            urgency = 1.0

        rank_score = round(
            (score * 0.4)
            + (priority_weight * 10 * 0.2)
            + (estimated_benefit / 10000 * 0.2)
            + (urgency * 10 * 0.2),
            2
        )

        ranked.append({
            "scheme": report["scheme"],
            "rank_score": rank_score
        })

    ranked.sort(key=lambda x: x["rank_score"], reverse=True)
    return ranked
