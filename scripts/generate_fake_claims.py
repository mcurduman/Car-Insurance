import json
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

NUM_CLAIMS = 200
claims = []
for _ in range(NUM_CLAIMS):
    claim_date = fake.date_between(start_date='-5y', end_date='today')
    claim = {
        "claim_number": fake.unique.bothify(text='CLM########'),
        "date": claim_date.isoformat(),
        "amount": round(random.uniform(100, 10000), 2),
        "status": random.choice(["open", "closed", "rejected"]),
        "description": fake.sentence()
    }
    claims.append(claim)

with open("fake_claims.json", "w") as f:
    json.dump(claims, f, indent=2)

print(f"Generated {NUM_CLAIMS} claims to fake_claims.json")
