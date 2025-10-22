
import pytest
from unittest.mock import patch
from app.utils import events

@patch('app.utils.events.log')
def test_policy_created(mock_log):
	events.policy_created('p1', 'c1', 'prod')
	mock_log.info.assert_called_once_with('policy_created', policy_id='p1', customer_id='c1', product='prod')

@patch('app.utils.events.log')
def test_policy_updated(mock_log):
	changes = {'field': 'value'}
	events.policy_updated('p2', changes)
	mock_log.info.assert_called_once_with('policy_updated', policy_id='p2', changes=changes)

@patch('app.utils.events.log')
def test_claim_created_default_currency(mock_log):
	events.claim_created('cl1', 'p3', 100.0)
	mock_log.info.assert_called_once_with('claim_created', claim_id='cl1', policy_id='p3', amount=100.0, currency='EUR')

@patch('app.utils.events.log')
def test_claim_created_custom_currency(mock_log):
	events.claim_created('cl2', 'p4', 200.0, currency='USD')
	mock_log.info.assert_called_once_with('claim_created', claim_id='cl2', policy_id='p4', amount=200.0, currency='USD')

@patch('app.utils.events.log')
def test_policy_expiry_detected_default_source(mock_log):
	events.policy_expiry_detected('p5', '2025-01-01')
	mock_log.info.assert_called_once_with('policy_expiry_detected', policy_id='p5', expires_at='2025-01-01', source='task_d')

@patch('app.utils.events.log')
def test_policy_expiry_detected_custom_source(mock_log):
	events.policy_expiry_detected('p6', '2025-01-02', source='manual')
	mock_log.info.assert_called_once_with('policy_expiry_detected', policy_id='p6', expires_at='2025-01-02', source='manual')
