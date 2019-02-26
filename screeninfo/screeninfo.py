import os

from screeninfo.common import ScreenInfoError
from screeninfo.enumerators import cygwin, drm, osx, windows, x11

_ENUMERATORS = {
    "windows": windows.enumerate,
    "cygwin": cygwin.enumerate,
    "x11": x11.enumerate,
    "drm": drm.enumerate,
    "osx": osx.enumerate,
}


def _get_enumerator():
    for enumerator in _ENUMERATORS.values():
        try:
            enumerator()
            return enumerator
        except Exception:
            pass
    raise ScreenInfoError("This environment is not supported.")


def get_monitors(name=None):
    """Returns a list of :class:`Monitor` objects based on active monitors."""
    enumerator = _ENUMERATORS[name] if name else _get_enumerator()
    return enumerator()
