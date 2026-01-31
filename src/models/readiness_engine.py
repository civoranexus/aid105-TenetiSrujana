def assess_application_readiness(required_documents, available_documents=None):
    if available_documents is None:
        available_documents = ["Aadhaar Card", "Residence Proof"]

    missing = [d for d in required_documents if d not in available_documents]

    readiness_score = int(
        (len(required_documents) - len(missing)) / len(required_documents) * 100
    )

    status = "READY TO APPLY" if readiness_score >= 90 else "NOT READY"

    advice = (
        "All mandatory documents are available. Proceed with application."
        if status == "READY TO APPLY"
        else "Complete missing documents before applying to avoid rejection."
    )

    return {
        "readiness_score": readiness_score,
        "status": status,
        "missing_documents": missing,
        "advice": advice
    }
