def simulate_income_scenarios(user_profile, scheme, income_variations):
    """
    Simulates eligibility score changes when income varies.
    """
    scenarios = []

    for income in income_variations:
        temp_user = user_profile.copy()
        temp_user["income"] = income

        min_i = scheme["min_income"]
        max_i = scheme["max_income"]

        eligible = min_i <= income <= max_i

        scenarios.append({
            "income": income,
            "eligible": eligible
        })

    return scenarios
