import json
from faker import Faker
import random

fake = Faker()

NUM_CARS = 200
cars = []
for _ in range(NUM_CARS):
    car = {
        "vin": fake.unique.bothify(text='?????????????????'),
        "make": fake.company(),
        "model": fake.word(),
        "year": random.randint(1990, 2023),
        "color": fake.color_name()
    }
    cars.append(car)

with open("fake_cars.json", "w") as f:
    json.dump(cars, f, indent=2)

print(f"Generated {NUM_CARS} cars to fake_cars.json")
