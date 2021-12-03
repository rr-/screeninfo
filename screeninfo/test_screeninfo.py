import os
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


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="GitHub actions have no physical monitors",
)
def test_get_monitors_has_at_least_one_monitor():
    assert len(list(get_monitors())) > 0
