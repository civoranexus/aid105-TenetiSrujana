def generate_action_plan(report, readiness):
    tasks_today = []
    tasks_next = []

    if report["priority"] == "APPLY IMMEDIATELY":
        for doc in readiness["missing_documents"]:
            tasks_today.append(f"Apply for {doc}")

        tasks_next.append("Submit application on official portal")

    elif report["priority"] == "PREPARE DOCUMENTS":
        for doc in readiness["missing_documents"]:
            tasks_next.append(f"Arrange {doc}")

    return {
        "today": tasks_today,
        "next": tasks_next,
        "risk": report["estimated_loss"]
    }
