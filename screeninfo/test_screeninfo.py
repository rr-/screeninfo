from contextlib import contextmanager

import pytest

from screeninfo import get_monitors, get_primary


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


def test_get_primary_does_not_raise():
    with not_raises(Exception):
        primary = get_primary()

        assert (primary[0] * 0, primary[1] * 0) == (0, 0)


def test_get_primary_has_two_values():
    assert len(tuple(get_primary())) == 2
