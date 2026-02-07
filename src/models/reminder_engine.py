from datetime import datetime, timedelta


def generate_reminder(report, readiness):
    """
    Generates smart reminders based on urgency, readiness, and priority
    """

    reminders = []

    urgency = report["urgency"]
    priority = report["priority"]
    scheme = report["scheme"]

    # 🔔 Reminder for urgent schemes
    if urgency in ["EXTREME", "HIGH"] and priority == "APPLY IMMEDIATELY":
        reminders.append({
            "type": "URGENT",
            "when": "Today",
            "message": f"Apply for {scheme} immediately to avoid missing the deadline."
        })

    # 📄 Reminder for missing documents
    if readiness["status"] == "NOT READY":
        reminders.append({
            "type": "DOCUMENT",
            "when": "Before Application",
            "message": "Complete missing documents to prevent application rejection."
        })

    # ⏰ Gentle reminder for medium priority schemes
    if priority == "PREPARE DOCUMENTS" and urgency in ["LOW", "MEDIUM"]:
        reminders.append({
            "type": "FOLLOW-UP",
            "when": "In 3 days",
            "message": f"Prepare documents for {scheme} and plan submission."
        })

    return reminders
