def validate_amount(v: float | None) -> float | None:
	if v is not None:
		if v <= 0:
			raise ValueError("Amount must be positive")
		if v > 1_000_000:
			raise ValueError("Amount must be less than or equal to 1,000,000")
	return v
