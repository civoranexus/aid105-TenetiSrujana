import csv
from models.eligibility_scoring import calculate_eligibility_score

user_profile = {
    "name": "Ravi",
    "income": 180000,
    "state": "Telangana",
    "category": "Student"
}

with open("src/data/schemes_master.csv", newline="") as file:
    reader = csv.DictReader(file)
    schemes = list(reader)

print("Eligibility Results:\n")

for scheme in schemes:
    scheme["min_income"] = int(scheme["min_income"])
    scheme["max_income"] = int(scheme["max_income"])

    result = calculate_eligibility_score(user_profile, scheme)

    print(f"Scheme: {scheme['scheme_name']}")
    print(f"Score: {result['score']}")
    print(f"Confidence: {result['confidence']}")
    print("Reasons:")
    for r in result["reasons"]:
        print(f" - {r}")
    print("-" * 50)
