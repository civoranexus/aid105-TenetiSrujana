def analyze_life_events(user_profile, life_events, scheme_name):
    insights = []

    if "student_passed_12th" in life_events:
        if "Scholarship" in scheme_name:
            insights.append(
                "Recent academic milestone increases relevance of education-related schemes."
            )

    if "student_passed_degree" in life_events:
        if "Loan" in scheme_name or "Employment" in scheme_name:
            insights.append(
                "Graduation event increases importance of career and self-employment schemes."
            )

    if "family_income_reduced" in life_events:
        insights.append(
            "Recent income reduction strengthens priority for income-sensitive welfare schemes."
        )

    if "marriage_planned" in life_events:
        if "Kalyana Lakshmi" in scheme_name:
            insights.append(
                "Upcoming marriage makes this scheme time-critical."
            )

    if "turned_senior_citizen" in life_events:
        if "Pension" in scheme_name:
            insights.append(
                "Age milestone activates senior citizen pension eligibility."
            )

    return insights
