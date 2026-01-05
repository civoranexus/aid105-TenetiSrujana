from datetime import datetime

def calculate_eligibility_score(user_profile, scheme):
    score = 0
    reasons = []

    # Income Match (40 points)
    if scheme["min_income"] <= user_profile["income"] <= scheme["max_income"]:
        score += 40
        reasons.append("Income falls within eligible range")
    else:
        reasons.append("Income does not meet eligibility criteria")

    # State Match (25 points)
    if scheme["state"] == "ALL" or scheme["state"] == user_profile["state"]:
        score += 25
        reasons.append("State eligibility matched")
    else:
        reasons.append("State eligibility not matched")

    # Category Match (20 points)
    if scheme["category"].lower() == user_profile["category"].lower():
        score += 20
        reasons.append("Category eligibility matched")

    # Deadline Urgency (15 points)
    today = datetime.today()
    deadline = datetime.strptime(scheme["deadline"], "%Y-%m-%d")
    days_left = (deadline - today).days

    if days_left <= 15:
        score += 15
        reasons.append("High urgency due to approaching deadline")
    elif days_left <= 30:
        score += 8
        reasons.append("Moderate urgency")

    # Confidence Level
    if score >= 75:
        confidence = "HIGH"
    elif score >= 50:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return {
        "score": score,
        "confidence": confidence,
        "reasons": reasons
    }
