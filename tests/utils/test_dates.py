
import pytest
from datetime import date
from app.utils.dates import (
    validate_date_range,
    validate_start_end_dates_optional,
    validate_start_end_dates,
    validate_data_in_interval,
    validate_data_in_interval_bool,
    validate_year_of_manufacture
)

def test_validate_date_range_valid():
    d = date(2000, 1, 1)
    assert validate_date_range(d) == d

def test_validate_date_range_invalid_low():
    d = date(1899, 1, 1)
    with pytest.raises(ValueError, match="must be between years 1900 and 2100"):
        validate_date_range(d)

def test_validate_date_range_invalid_high():
    d = date(2101, 1, 1)
    with pytest.raises(ValueError, match="must be between years 1900 and 2100"):
        validate_date_range(d)

def test_validate_date_range_custom_field():
    d = date(1899, 1, 1)
    with pytest.raises(ValueError, match="custom must be between years 1900 and 2100"):
        validate_date_range(d, field_name="custom")

def test_validate_start_end_dates_optional_valid():
    start = date(2020, 1, 1)
    end = date(2021, 1, 1)
    assert validate_start_end_dates_optional(start, end) is None
    assert validate_start_end_dates_optional(None, end) is None
    assert validate_start_end_dates_optional(start, None) is None
    assert validate_start_end_dates_optional(None, None) is None

def test_validate_start_end_dates_optional_invalid():
    start = date(2021, 1, 1)
    end = date(2020, 1, 1)
    with pytest.raises(ValueError, match="end_date must be after start_date"):
        validate_start_end_dates_optional(start, end)

def test_validate_start_end_dates_valid():
    start = date(2020, 1, 1)
    end = date(2021, 1, 1)
    assert validate_start_end_dates(start, end) is None

def test_validate_start_end_dates_invalid():
    start = date(2021, 1, 1)
    end = date(2020, 1, 1)
    with pytest.raises(ValueError, match="end_date must be after start_date"):
        validate_start_end_dates(start, end)

def test_validate_data_in_interval_valid():
    start = date(2020, 1, 1)
    end = date(2021, 1, 1)
    d = date(2020, 6, 1)
    assert validate_data_in_interval(d, start, end) == d

def test_validate_data_in_interval_invalid():
    start = date(2020, 1, 1)
    end = date(2021, 1, 1)
    d = date(2019, 12, 31)
    with pytest.raises(ValueError, match="date must be between"):
        validate_data_in_interval(d, start, end)

def test_validate_data_in_interval_custom_field():
    start = date(2020, 1, 1)
    end = date(2021, 1, 1)
    d = date(2019, 12, 31)
    with pytest.raises(ValueError, match="custom must be between"):
        validate_data_in_interval(d, start, end, field_name="custom")

def test_validate_data_in_interval_bool_true():
    start = date(2020, 1, 1)
    end = date(2021, 1, 1)
    d = date(2020, 6, 1)
    assert validate_data_in_interval_bool(d, start, end)

def test_validate_data_in_interval_bool_false():
    start = date(2020, 1, 1)
    end = date(2021, 1, 1)
    d = date(2019, 12, 31)
    assert not validate_data_in_interval_bool(d, start, end)

def test_validate_year_of_manufacture_valid():
    y = 2000
    assert validate_year_of_manufacture(y) == y

def test_validate_year_of_manufacture_invalid_low():
    y = 1885
    import re
    with pytest.raises(ValueError, match=r"year_of_manufacture must be between 1886"):
        validate_year_of_manufacture(y)

def test_validate_year_of_manufacture_invalid_high():
    y = date.today().year + 1
    import re
    with pytest.raises(ValueError, match=r"year_of_manufacture must be between 1886"):
        validate_year_of_manufacture(y)
        