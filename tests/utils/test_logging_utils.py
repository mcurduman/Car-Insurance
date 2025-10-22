import pytest
from unittest.mock import patch
from app.utils.logging_utils import log_event

@patch('app.utils.logging_utils.log')
def test_sync_success(mock_log):
    @log_event('sync_event')
    def f(x):
        return x + 1
    result = f(2)
    assert result == 3
    mock_log.info.assert_any_call('sync_event_started')
    assert any(call[0][0] == 'sync_event_completed' for call in mock_log.info.call_args_list)

@patch('app.utils.logging_utils.log')
def test_sync_error(mock_log):
    @log_event('sync_event')
    def f(x):
        raise ValueError('fail')
    with pytest.raises(ValueError):
        f(1)
    mock_log.error.assert_called()
    assert any('sync_event_failed' in str(call) for call in mock_log.error.call_args_list)

@patch('app.utils.logging_utils.log')
def test_sync_include_args(mock_log):
    @log_event('sync_event', include_args=True)
    def f(x, y=2):
        return x + y
    f(1, y=3)
    mock_log.info.assert_any_call('sync_event_started', args=(1,), kwargs={'y': 3})

@patch('app.utils.logging_utils.log')
def test_sync_custom_level(mock_log):
    @log_event('sync_event', level='warning')
    def f(x):
        return x
    f(1)
    mock_log.warning.assert_called()
    assert any('sync_event_completed' in str(call) for call in mock_log.warning.call_args_list)

@patch('app.utils.logging_utils.log')
def test_async_success(mock_log):
    import asyncio
    @log_event('async_event')
    async def f(x):
        return x + 1
    result = asyncio.run(f(2))
    assert result == 3
    mock_log.info.assert_any_call('async_event_started')
    assert any('async_event_completed' in str(call) for call in mock_log.info.call_args_list)

@patch('app.utils.logging_utils.log')
def test_async_error(mock_log):
    import asyncio
    @log_event('async_event')
    async def f(x):
        raise RuntimeError('fail')
    with pytest.raises(RuntimeError):
        asyncio.run(f(1))
    mock_log.error.assert_called()
    assert any('async_event_failed' in str(call) for call in mock_log.error.call_args_list)

@patch('app.utils.logging_utils.log')
def test_async_include_args(mock_log):
    import asyncio
    @log_event('async_event', include_args=True)
    async def f(x, y=2):
        return x + y
    asyncio.run(f(1, y=3))
    mock_log.info.assert_any_call('async_event_started', args=(1,), kwargs={'y': 3})

@patch('app.utils.logging_utils.log')
def test_async_custom_level(mock_log):
    import asyncio
    @log_event('async_event', level='warning')
    async def f(x):
        return x
    asyncio.run(f(1))
    mock_log.warning.assert_called()
    assert any('async_event_completed' in str(call) for call in mock_log.warning.call_args_list)
