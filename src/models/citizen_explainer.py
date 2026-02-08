def generate_citizen_summary(report):
    scheme = report["scheme"]
    priority = report["priority"]

    if priority == "APPLY IMMEDIATELY":
        return (
            f"You should apply for {scheme} immediately. "
            f"You meet eligibility criteria and delaying may cause loss of benefits."
        )

    elif priority == "PREPARE DOCUMENTS":
        return (
            f"You are likely eligible for {scheme}. "
            f"Prepare the required documents and apply soon."
        )

    else:
        return (
            f"{scheme} is currently not recommended. "
            f"Eligibility conditions are not fully met."
        )
