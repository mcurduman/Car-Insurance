

import pytest
from app.utils.amount import validate_amount

def test_validate_amount_valid():
	assert validate_amount(100.0) == 100.0
	assert validate_amount(1_000_000) == 1_000_000

def test_validate_amount_none():
	assert validate_amount(None) is None

def test_validate_amount_zero():
	with pytest.raises(ValueError, match="Amount must be positive"):
		validate_amount(0)

def test_validate_amount_negative():
	with pytest.raises(ValueError, match="Amount must be positive"):
		validate_amount(-10)

def test_validate_amount_over_max():
	with pytest.raises(ValueError, match="Amount must be less than or equal to 1,000,000"):
		validate_amount(1_000_001)