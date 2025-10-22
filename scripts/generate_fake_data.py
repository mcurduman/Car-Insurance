import json
from faker import Faker

fake = Faker()

NUM_USERS = 200
users = []
for _ in range(NUM_USERS):
    users.append({
        "username": fake.user_name(),
        "email": fake.unique.email(),
        "hashed_password": fake.sha256()
    })

with open("scripts/fake_users.json", "w") as f:
    json.dump(users, f, indent=2)

print(f"Generated {NUM_USERS} fake users in scripts/fake_users.json")
