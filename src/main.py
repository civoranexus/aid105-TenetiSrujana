import csv

from models.eligibility_scoring import calculate_eligibility_score
from models.recommendation_advisor import generate_recommendation_report
from models.ranking_engine import rank_schemes
from models.decision_trace_engine import generate_decision_trace
from models.citizen_explainer import generate_citizen_summary
from models.life_event_engine import analyze_life_events
from models.readiness_engine import assess_application_readiness
from models.fairness_engine import audit_fairness
from models.action_planner import generate_action_plan
from models.reminder_engine import generate_reminder
from models.impact_engine import generate_impact_summary
from models.policy_simulator import simulate_policy_change


# ---------------- USER PROFILE ----------------
user_profile = {
    "name": "Ravi",
    "income": 180000,
    "state": "Telangana",
    "category": "Student"
}

# ---------------- LIFE EVENTS ----------------
life_events = [
    "student_passed_12th",
    "family_income_reduced"
]

eligibility_results = []
enriched_reports = []
last_report = None


# ---------------- LOAD SCHEME DATA ----------------
with open("src/data/schemes_master.csv", newline="") as file:
    reader = csv.DictReader(file)
    schemes = list(reader)

print("\n🔍 AI Eligibility & Risk Analysis Report\n")


# ---------------- ELIGIBILITY COMPUTATION ----------------
for scheme in schemes:
    scheme["min_income"] = int(scheme["min_income"])
    scheme["max_income"] = int(scheme["max_income"])
    scheme["estimated_benefit"] = int(scheme["estimated_benefit"])
    scheme["priority_weight"] = int(scheme["priority_weight"])

    result = calculate_eligibility_score(user_profile, scheme)
    result["scheme"] = scheme["scheme_name"]
    result["scheme_data"] = scheme

    eligibility_results.append(result)


# ---------------- DETAILED AI REPORTS ----------------
for result in eligibility_results:
    report = generate_recommendation_report(result)
    last_report = report  # save for impact summary

    print(f"🏷️ Scheme: {report['scheme']}")
    print(f"📊 Score: {report['score']} | Confidence: {report['confidence']}")
    print(f"🚦 Priority: {report['priority']}")
    print(f"⏱️ Urgency: {report['urgency']} | Risk: {report['risk_level']}")
    print(f"{report['warning']}")
    print(f"💸 {report['estimated_loss']}")

    print("Reasons:")
    for r in report["reasons"]:
        print(f" - {r}")

    print("Required Documents:")
    for d in report["required_documents"]:
        print(f" - {d}")

    # ---------------- Explainable AI ----------------
    trace = generate_decision_trace(result)
    summary = generate_citizen_summary(report)

    print("\n🧠 AI Decision Trace:")
    for t in trace:
        print(f" - {t}")

    print("\n👤 Citizen-Friendly Explanation:")
    print(f" {summary}")

    # ---------------- Application Readiness ----------------
    readiness = assess_application_readiness(report["required_documents"])

    print("\n📋 Application Readiness Check:")
    print(f"Status: {readiness['status']}")
    print(f"Readiness Score: {readiness['readiness_score']}%")

    if readiness["missing_documents"]:
        print("Missing Items:")
        for m in readiness["missing_documents"]:
            print(f" - {m}")

    print("AI Advice:")
    print(f" {readiness['advice']}")

    # ---------------- Action Planner ----------------
    action_plan = generate_action_plan(report, readiness)

    print("\n📅 AI APPLICATION ACTION PLAN")
    for t in action_plan.get("today", []):
        print(f" - {t}")
    for n in action_plan.get("next", []):
        print(f" - {n}")

    # ---------------- Reminder Engine ----------------
    reminders = generate_reminder(report, readiness)
    for r in reminders:
        print(f"🔔 {r['message']}")

    # ---------------- Life Events ----------------
    insights = analyze_life_events(user_profile, life_events, report["scheme"])
    for i in insights:
        print(f"🧠 {i}")

    print("=" * 70)

    enriched_reports.append({
        "scheme": report["scheme"],
        "score": report["score"],
        "priority_weight": result["scheme_data"]["priority_weight"],
        "deadline": result["scheme_data"]["deadline"],
        "estimated_benefit": result["scheme_data"]["estimated_benefit"],
        "category": result["scheme_data"]["category"]
    })


# ---------------- FINAL AI RANKING ----------------
print("\n🏆 AI FINAL APPLICATION PRIORITY RANKING\n")
ranked = rank_schemes(enriched_reports)

for i, r in enumerate(ranked, 1):
    print(f"{i}. {r['scheme']} (Rank Score: {r['rank_score']})")


# ---------------- FAIRNESS AUDIT ----------------
print("\n⚖️ AI FAIRNESS & BIAS AUDIT\n")
for f in audit_fairness(enriched_reports):
    print(f)


# ---------------- CITIZEN IMPACT SUMMARY ----------------
if last_report:
    impact = generate_impact_summary(last_report)
    print("\n🎯 Citizen Impact Summary")
    print(f"Financial Impact: {impact['financial_impact']}")
    print(f"Outcome: {impact['outcome']}")


# ---------------- DAY 7: POLICY CHANGE SIMULATOR ----------------
print("\n📜 AI POLICY CHANGE IMPACT SIMULATION\n")

policy_changes = {
    "max_income": 250000,
    "category": "Student",
    "deadline_extension_days": 30
}

for scheme in schemes:
    result = simulate_policy_change(scheme, policy_changes)

    print(f"🏷️ Scheme: {result['scheme']}")
    for i in result["impact_analysis"]:
        print(f" - {i}")
    print("-" * 50)
