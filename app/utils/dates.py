from datetime import date

def validate_date_range(d: date, field_name: str = "date") -> date:
    if not (1900 <= d.year <= 2100):
        raise ValueError(f"{field_name} must be between years 1900 and 2100")
    return d

def validate_start_end_dates_optional(start_date: date | None, end_date: date | None) -> None:
    if start_date is not None and end_date is not None:
        if end_date <= start_date:
            raise ValueError("end_date must be after start_date")
        
def validate_start_end_dates(start_date: date, end_date: date) -> None:
    if end_date <= start_date:
        raise ValueError("end_date must be after start_date")
    
    
def validate_data_in_interval(d: date, start_date: date, end_date: date, field_name: str = "date") -> date:
    if not (start_date <= d <= end_date):
        raise ValueError(f"{field_name} must be between {start_date} and {end_date}")
    return d

def validate_data_in_interval_bool(d: date, start_date: date, end_date: date, field_name: str = "date") -> bool:
    if not (start_date <= d <= end_date):
        return False
    return True

def validate_year_of_manufacture(year: int) -> int:
    current_year = date.today().year
    if not (1886 <= year <= current_year):  # First car invented in 1886
        raise ValueError(f"year_of_manufacture must be between 1886 and {current_year}")
    return year