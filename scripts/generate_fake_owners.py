import json
from faker import Faker

fake = Faker()

NUM_OWNERS = 200
owners = []
for _ in range(NUM_OWNERS):
    owner = {
        "name": fake.name(),
        "email": fake.unique.email(),
        "address": fake.address().replace('\n', ', '),
        "phone": fake.phone_number()
    }
    owners.append(owner)

with open("fake_owners.json", "w") as f:
    json.dump(owners, f, indent=2)

print(f"Generated {NUM_OWNERS} owners to fake_owners.json")
