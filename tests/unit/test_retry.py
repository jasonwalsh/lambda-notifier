from unittest.mock import Mock, call, patch

from functions.retry import Retry


@patch('functions.retry.sleep', autospec=True)
@patch('functions.retry.logging', autospec=True)
def test_retry(logging, sleep):
    retry = Retry(interval=1, max_retries=3)
    action = Mock(side_effect=ZeroDivisionError)

    retry(action)

    assert sleep.call_args == call(1)
    assert action.call_count == 4
    assert retry.retries == 3
    assert retry.errors == 4

    assert logging.error.call_count == 4
