def generate_overall_summary(enriched_reports):
    total = len(enriched_reports)

    closed = [
        r for r in enriched_reports
        if r["score"] < 50
    ]

    actionable = [
        r for r in enriched_reports
        if r["score"] >= 50
    ]

    top_actions = []
    for r in actionable[:3]:
        top_actions.append(f"Focus on {r['scheme']}")

    if not top_actions:
        top_actions.append("No schemes available for immediate action")

    return {
        "total_schemes": total,
        "actionable": len(actionable),
        "closed": len(closed),
        "actions": top_actions,
        "risk": "Multiple benefits may be lost due to delays or missing documents."
    }
