from contextlib import contextmanager
from unittest import mock

import pytest

from screeninfo import Enumerator, Monitor, ScreenInfoError, get_monitors


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail("DID RAISE {0}".format(exception))


def test_get_monitors_without_enumerators():
    with mock.patch(
        "screeninfo.screeninfo.ENUMERATOR_MAP", {}
    ) as mock_get_monitors:
        with pytest.raises(ScreenInfoError):
            get_monitors()


def test_get_monitors_handles_faulty_enumerator():
    enumerator = mock.Mock(
        enumerate_monitors=mock.Mock(side_effect=ImportError)
    )
    with mock.patch(
        "screeninfo.screeninfo.ENUMERATOR_MAP",
        {Enumerator.Windows: enumerator},
    ):
        with pytest.raises(ScreenInfoError):
            get_monitors()
        enumerator.enumerate_monitors.assert_called_once()


def test_get_monitors_ignores_enumerator_that_produces_no_results():
    enumerator = mock.Mock(enumerate_monitors=mock.Mock(return_value=[]))
    with mock.patch(
        "screeninfo.screeninfo.ENUMERATOR_MAP",
        {Enumerator.Windows: enumerator},
    ):
        with pytest.raises(ScreenInfoError):
            get_monitors()
        enumerator.enumerate_monitors.assert_called_once()


def test_get_monitors_uses_working_enumerator():
    enumerator = mock.Mock(
        enumerate_monitors=mock.Mock(
            return_value=[Monitor(x=0, y=0, width=800, height=600)]
        )
    )
    with mock.patch(
        "screeninfo.screeninfo.ENUMERATOR_MAP",
        {Enumerator.Windows: enumerator},
    ) as mock_get_monitors:
        monitors = get_monitors()
        assert len(monitors) == 1
        assert monitors[0].x == 0
        assert monitors[0].y == 0
        assert monitors[0].width == 800
        assert monitors[0].height == 600
        enumerator.enumerate_monitors.assert_called_once()


def test_get_monitors_uses_first_working_enumerator():
    enumerator1 = mock.Mock(
        enumerate_monitors=mock.Mock(side_effect=ImportError)
    )
    enumerator2 = mock.Mock(
        enumerate_monitors=mock.Mock(
            return_value=[Monitor(x=0, y=0, width=800, height=600)]
        )
    )
    enumerator3 = mock.Mock(
        enumerate_monitors=mock.Mock(side_effect=ImportError)
    )
    with mock.patch(
        "screeninfo.screeninfo.ENUMERATOR_MAP",
        {
            Enumerator.Windows: enumerator1,
            Enumerator.Xinerama: enumerator2,
            Enumerator.DRM: enumerator3,
        },
    ) as mock_get_monitors:
        monitors = get_monitors()
        assert len(monitors) == 1
        assert monitors[0].x == 0
        assert monitors[0].y == 0
        assert monitors[0].width == 800
        assert monitors[0].height == 600
        enumerator1.enumerate_monitors.assert_called_once()
        enumerator2.enumerate_monitors.assert_called_once()
        enumerator3.enumerate_monitors.assert_not_called()


@pytest.mark.parametrize("param", ["windows", Enumerator.Windows])
def test_get_monitors_with_concrete_enumerator(param):
    enumerator = mock.Mock(
        enumerate_monitors=mock.Mock(
            return_value=[Monitor(x=0, y=0, width=800, height=600)]
        )
    )
    with mock.patch(
        "screeninfo.screeninfo.ENUMERATOR_MAP",
        {Enumerator.Windows: enumerator},
    ) as mock_get_monitors:
        monitors = get_monitors(param)
        assert len(monitors) == 1
        assert monitors[0].x == 0
        assert monitors[0].y == 0
        assert monitors[0].width == 800
        assert monitors[0].height == 600
        enumerator.enumerate_monitors.assert_called_once()


def test_get_monitors_with_invalid_enumerator():
    enumerator = mock.Mock(
        enumerate_monitors=mock.Mock(
            return_value=[Monitor(x=0, y=0, width=800, height=600)]
        )
    )
    with mock.patch(
        "screeninfo.screeninfo.ENUMERATOR_MAP",
        {Enumerator.Windows: enumerator},
    ) as mock_get_monitors:
        with pytest.raises(ValueError):
            monitors = get_monitors("Invalid")


def test_get_monitors_with_unlisted_enumerator():
    enumerator = mock.Mock(
        enumerate_monitors=mock.Mock(
            return_value=[Monitor(x=0, y=0, width=800, height=600)]
        )
    )
    with mock.patch(
        "screeninfo.screeninfo.ENUMERATOR_MAP",
        {Enumerator.Windows: enumerator},
    ) as mock_get_monitors:
        with pytest.raises(KeyError):
            monitors = get_monitors(Enumerator.OSX)
