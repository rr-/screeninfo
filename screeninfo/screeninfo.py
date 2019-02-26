import importlib

from screeninfo.common import Enumerator, ScreenInfoError

_ENUMERATORS = {
    Enumerator.Windows.value: "screeninfo.enumerators.windows",
    Enumerator.Cygwin.value: "screeninfo.enumerators.cygwin",
    Enumerator.X11.value: "screeninfo.enumerators.x11",
    Enumerator.DRM.value: "screeninfo.enumerators.drm",
    Enumerator.OSX.value: "screeninfo.enumerators.osx",
}


def _get_monitors(enumerator_module_path):
    module = importlib.import_module(enumerator_module_path)
    return module.enumerate_monitors()


def get_monitors(name=None):
    """Returns a list of :class:`Monitor` objects based on active monitors."""
    if name is not None:
        if name not in _ENUMERATORS:
            raise ScreenInfoError("Unknown enumerator: " + name)

        return _get_monitors(_ENUMERATORS[name])

    for module_path in _ENUMERATORS.values():
        try:
            return _get_monitors(module_path)
        except Exception:
            pass
    raise ScreenInfoError("No enumerators available")
