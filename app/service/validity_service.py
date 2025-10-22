from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.policy_repository import PolicyRepository
from app.db.repositories.car_repository import CarRepository
from datetime import date
from app.utils.dates import validate_data_in_interval_bool


class ValidityService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_valid(self, car_id: int, date: date) -> bool:
        # Get the car by ID
        policies = await PolicyRepository(self.session).get_policies_by_car_id(car_id)
        #check for non expired policies -> logged_expiry_at is null
        not_expired_policies = [policy for policy in policies if policy.logged_expiry_at is None]
        for policy in not_expired_policies:
            if validate_data_in_interval_bool(date, policy.start_date, policy.end_date):
                return True 
        return False
