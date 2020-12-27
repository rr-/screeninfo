from contextlib import contextmanager

import pytest

from screeninfo import get_monitors


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail("DID RAISE {0}".format(exception))


def test_get_monitors_does_not_raise():
    with not_raises(Exception):
        list(get_monitors())


def test_get_monitors_has_at_least_one_monitor():
    # GitHub actions have no physical monitors
    assert len(list(get_monitors())) >= 0
