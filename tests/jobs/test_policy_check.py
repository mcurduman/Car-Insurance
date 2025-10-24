import pytest
from unittest.mock import ANY
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, date, time
import jobs.policy_check as policy_check

class DummyPolicy:
    def __init__(self, id=1, car_id=101, provider="TestProvider", end_date=None, logged_expiry_at=None):
        self.id = id
        self.car_id = car_id
        self.provider = provider
        self.end_date = end_date or date.today()
        self.logged_expiry_at = logged_expiry_at

@pytest.mark.asyncio
@patch("jobs.policy_check.log_info")
@patch("app.db.session.AsyncSessionLocal")
@patch("jobs.policy_check.PolicyRepository")
@patch("jobs.policy_check.now_tz")
async def test_policy_expiry_processes_expired_policy(
    mock_now_tz, mock_repo_cls, mock_session_cls, mock_log_info
):
    from zoneinfo import ZoneInfo
    tz = ZoneInfo(policy_check.TIMEZONE)
    now = datetime(2025, 10, 23, 6, 30, tzinfo=tz)
    mock_now_tz.return_value = now
    mock_session = MagicMock()
    mock_session_cls.return_value.__aenter__.return_value = mock_session

    dummy_policy = DummyPolicy(id=42, car_id=123, provider="MockProvider", end_date=now.date(), logged_expiry_at=None)
    mock_repo = MagicMock()
    mock_repo.get_policies_not_logged_expiry = MagicMock(return_value=[dummy_policy])
    mock_repo.update_policy_logged_expiry = MagicMock(return_value=dummy_policy)
    mock_repo_cls.return_value = mock_repo

    await policy_check.check_policy_expiry()

    mock_repo.update_policy_logged_expiry.assert_called_once_with(42, now.date())
    mock_log_info.assert_any_call("policy_expiry_processing", policy_id=42, car_id=123, end_date=str(now.date()))
    mock_log_info.assert_any_call("policy_expiry_logged", policy_id=42, logged_at=now.isoformat())

@pytest.mark.asyncio
@patch("jobs.policy_check.log_info")
@patch("app.db.session.AsyncSessionLocal")
@patch("app.db.repositories.policy_repository.PolicyRepository.get_policies_not_logged_expiry", return_value=[])
@patch("app.db.repositories.policy_repository.PolicyRepository.update_policy_logged_expiry", return_value=None)
@patch("app.db.repositories.policy_repository.PolicyRepository")
@patch("jobs.policy_check.now_tz")
async def test_policy_expiry_skipped_outside_window(mock_now_tz, mock_repo_cls, mock_update_policy, mock_get_policies, mock_session_cls, mock_log_info):
    # Window is 4:00-10:00, test at 2:00 (outside)
    from zoneinfo import ZoneInfo
    tz = ZoneInfo(policy_check.TIMEZONE)
    now = datetime(2025, 10, 23, 2, 0, tzinfo=tz)
    mock_now_tz.return_value = now
    mock_session = MagicMock()
    mock_session_cls.return_value.__aenter__.return_value = mock_session
    mock_repo = MagicMock()
    mock_repo_cls.return_value = mock_repo

    await policy_check.check_policy_expiry()
    mock_log_info.assert_any_call("policy_expiry_tick", ts=now.isoformat(), interval_min=policy_check.JOB_INTERVAL_MINUTES)
    mock_log_info.assert_any_call("policy_expiry_skipped_outside_window", now=now.isoformat(), window=ANY)
    mock_repo.get_policies_not_logged_expiry.assert_not_called()

@pytest.mark.asyncio
@patch("jobs.policy_check.log_info")
@patch("jobs.policy_check.now_tz")
@patch("app.db.repositories.policy_repository.PolicyRepository.get_policies_not_logged_expiry", return_value=[])
@patch("app.db.repositories.policy_repository.PolicyRepository.update_policy_logged_expiry", return_value=None)
async def test_policy_expiry_worker_start_and_stop(mock_update_policy, mock_get_policies, mock_now_tz, mock_log_info):
    # Test worker start/stop logic
    from zoneinfo import ZoneInfo
    tz = ZoneInfo(policy_check.TIMEZONE)
    now = datetime(2025, 10, 23, 6, 0, tzinfo=tz)
    mock_now_tz.return_value = now
    import jobs.policy_check as pc
    with patch("jobs.policy_check.AsyncIOScheduler") as mock_scheduler:
        instance = mock_scheduler.return_value
        instance.add_job.return_value = None
        instance.start.return_value = None
        with patch("asyncio.Event") as mock_event:
            mock_event.return_value.wait.side_effect = KeyboardInterrupt
            try:
                await pc.main()
            except KeyboardInterrupt:
                pass
    mock_log_info.assert_any_call("policy_expiry_worker_starting", tz=pc.TIMEZONE, interval_min=pc.JOB_INTERVAL_MINUTES)
    mock_log_info.assert_any_call("policy_expiry_worker_started")

