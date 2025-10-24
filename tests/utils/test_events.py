import pytest
from unittest.mock import patch
from app.utils import events

@patch('app.utils.events.log')
def test_policy_created(mock_log):
    events.policy_created(1, 2,"provider",'2025-01-01', '2025-12-31')
    mock_log.info.assert_called_once_with(
        'policy_created',
        policy_id=1,
        car_id=2,
        provider="provider",
        start_date='2025-01-01',
        end_date='2025-12-31'
    )

@patch('app.utils.events.log')
def test_policy_updated(mock_log):
    changes = {'field': 'value'}
    events.policy_updated(policy_id=3, car_id=4, provider="provider", start_date='2025-02-01', end_date='2025-11-30', changes=changes)
    mock_log.info.assert_called_once_with(
        'policy_updated',
        policy_id=3,
        car_id=4,
        provider="provider",
        start_date='2025-02-01',
        end_date='2025-11-30',
        changes=changes
    )

@patch('app.utils.events.log')
def test_claim_created(mock_log):
    events.claim_created(claim_id=5, car_id=6, amount=100.0)
    mock_log.info.assert_called_once_with(
        'claim_created',
        claim_id=5,
        car_id=6,
        amount=100.0
    )

@patch('app.utils.events.log')
def test_policy_expiry_detected_default_source(mock_log):
    events.policy_expiry_detected(policy_id=7, car_id=8, start_date='2025-03-01', end_date='2025-10-31', expires_at='2025-10-31', source='task_d', provider="provider")
    mock_log.info.assert_called_once_with(
        'policy_expiry_detected',
		policy_id=7,
		car_id=8,
		start_date='2025-03-01',
		end_date='2025-10-31',
		expires_at='2025-10-31',
		source='task_d',
		provider="provider"
	)

@patch('app.utils.events.log')
def test_policy_expiry_detected_custom_source(mock_log):
    events.policy_expiry_detected(policy_id=9, car_id=10, start_date='2025-04-01', end_date='2025-09-30', expires_at='2025-09-30', source='custom_source', provider="provider")
    mock_log.info.assert_called_once_with(
        'policy_expiry_detected',
		policy_id=9,
		car_id=10,
		start_date='2025-04-01',
		end_date='2025-09-30',
		expires_at='2025-09-30',
		source='custom_source',
		provider="provider"
	)
