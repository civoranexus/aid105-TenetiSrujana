def calculate_eligibility_score(user, scheme):
    score = 0
    reasons = []

    # Income match (weighted)
    if scheme["min_income"] <= user["income"] <= scheme["max_income"]:
        score += 40
        reasons.append("Income falls within eligible range")
    else:
        reasons.append("Income outside eligible range")

    # State match
    if scheme["scheme_state"] == "ALL":
        score += 10
        reasons.append("Scheme applicable nationwide")
    elif scheme["scheme_state"] == user["state"]:
        score += 25
        reasons.append("State eligibility matched")
    else:
        reasons.append("State eligibility not matched")

    # Category match
    if scheme["category"] == user["category"]:
        score += 25
        reasons.append("Category eligibility matched")
    else:
        reasons.append("Category eligibility not matched")

    # Priority weight influence
    score += scheme["priority_weight"]

    score = min(score, 100)

    return {
        "score": score if score >= 40 else 0,   # 👈 HARD REALISTIC CUTOFF
        "confidence": "HIGH" if score >= 80 else "MEDIUM" if score >= 60 else "LOW",
        "reasons": reasons
    }
