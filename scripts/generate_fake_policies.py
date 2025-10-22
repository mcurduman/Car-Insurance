import json
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

NUM_POLICIES = 200
policies = []
for _ in range(NUM_POLICIES):
    start_date = fake.date_between(start_date='-5y', end_date='today')
    end_date = start_date + timedelta(days=random.randint(30, 365))
    policy = {
        "policy_number": fake.unique.bothify(text='POL########'),
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "premium": round(random.uniform(200, 2000), 2),
        "status": random.choice(["active", "expired", "cancelled"])
    }
    policies.append(policy)

with open("fake_policies.json", "w") as f:
    json.dump(policies, f, indent=2)

print(f"Generated {NUM_POLICIES} policies to fake_policies.json")
