def simulate_policy_change(scheme, changes):
    impact = []

    if "max_income" in changes:
        old = int(scheme["max_income"])
        new = changes["max_income"]

        if new > old:
            impact.append("More citizens become eligible due to increased income limit.")
        else:
            impact.append("Some citizens may lose eligibility due to reduced income limit.")

    if "category" in changes:
        impact.append(f"Eligibility category expanded to {changes['category']}.")

    if "deadline_extension_days" in changes:
        impact.append(
            f"Deadline extended by {changes['deadline_extension_days']} days, reducing urgency risk."
        )

    return {
        "scheme": scheme["scheme_name"],
        "impact_analysis": impact
    }
