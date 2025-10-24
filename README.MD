Car Insurance Project
====================

The Car Insurance API is designed to manage comprehensive information about car owners, their vehicles, and related insurance policies. It empowers authorized users—such as insurance agents and internal systems—to:

- Record and verify vehicle insurance data
- Manage insurance claims efficiently
- Retrieve detailed car and policy history

This system ensures data consistency, reliability, and secure access for all insurance operations.

## Project Structure & Technologies

**Tech Stack:**
- Python 3.11+
- FastAPI (API framework)
- SQLAlchemy (async ORM)
- Alembic (migrations)
- PostgreSQL (production DB)
- SQLite (development DB)
- Docker & Docker Compose
- pytest (testing)
- asyncpg (PostgreSQL async driver)
- Pydantic (validation, settings)

**Main Folders:**
```
Car_Insurance/
├── alembic.ini
├── Dockerfile
├── requirements.txt
├── .env.production
├── .env.development
├── README.MD
├── alembic/
│   ├── env.py
│   ├── versions/
│   └── ...
├── app/
│   ├── main.py
│   ├── core/
│   ├── db/
│   ├── service/
│   ├── schemas/
│   ├── api/
│   ├── auth/
│   ├── utils/
│   └── ...
├── deployment/
│   ├── docker-compose.prod.yml
│   ├── docker-compose.dev.yml
│   └── ...
├── logs/
├── scripts/
│   ├── populate_prod.py
│   └── ...
├── tests/
│   ├── jobs/
│   ├── apis/
│   └── ...
```

**Key Components:**
- `app/main.py`: FastAPI entrypoint
- `app/service/`: Business logic/services
- `app/schemas/`: Pydantic models
- `app/db/`: DB session, models, repositories
- `alembic/`: Migrations
- `deployment/docker-compose.prod.yml`: Production orchestration
- `.env.production`: Production environment variables
- `tests/`: Unit/integration tests

**Usage:**
- Run with Docker Compose: `docker-compose -f deployment/docker-compose.prod.yml up --build -d`
- Testing: `pytest`

**Notes:**
- PostgreSQL for production, SQLite for local/dev (if configured)
- All services/scripts use async SQLAlchemy sessions
- Environment variables loaded from `.env.production`
- Healthchecks for all major services

---

## Requirements Compliance

### 3.1. Core Functionalities (Expanded Details)

1. **List all cars and their current owners**
   - The `/api/cars/` endpoint returns a list of all cars, each including its current owner’s name, contact information, and unique owner ID.
   - The `/api/cars/{car_id}` endpoint provides a complete profile for a specific car, including technical details (VIN, make, model, year) and a nested owner object.
   - Data is always up-to-date, reflecting ownership changes immediately.

2. **Check insurance validity**
   - The `/api/validity/` endpoint requires `carId` and a date (`YYYY-MM-DD`).
   - The system checks all policies for the car and determines if any are valid on the given date.
   - If the car or date is invalid, the API returns a clear error (e.g., 404 for missing car, 400 for bad date).
   - Example response: `{ "carId": 123, "date": "2025-10-24", "valid": true }`

3. **Register an insurance claim**
   - The `/api/claims/` endpoint validates all required fields: `claimDate` (ISO date), `description` (string), and `amount` (positive float).
   - Claims are only accepted for cars that exist in the system.
   - On success, the API returns a confirmation object with all claim details and a unique claim ID.
   - Example response: `{ "claimId": 456, "carId": 123, "claimDate": "2025-10-24", "description": "Accident", "amount": 1200.00 }`

4. **Retrieve a car’s history**
   - The `/api/history/{car_id}` endpoint returns a chronological list of all insurance policies and claims for the car.
   - Each event includes metadata: event type, date, provider, amount, and related policy/claim IDs.
   - History is comprehensive, including events from previous owners.

### 3.2. Validation Rules

- Every insurance policy requires a `startDate` and a non-null `endDate`.
- `endDate` must not precede `startDate`.
- API calls referencing non-existent `carId` return a 404 error.
- Dates follow ISO format `YYYY-MM-DD` and are validated to be between 1900–2100.
- Monetary values (claims) must be positive and within a reasonable range.

### 3.3. Automatic and Background Processes

- The system automatically detects expired policies and logs a message within 1 hour after expiry:
  - “Policy {id} for car {carId} expired on {endDate}”
- Each policy’s expiry is logged only once, even if the process runs repeatedly.

### 3.4. Data Integrity Requirements

- Policies always belong to an existing car.
- Cars always have a valid owner reference.
- Claims always belong to an existing car.
- Deleting a car cascades deletes its policies and claims, or is explicitly restricted.

---

