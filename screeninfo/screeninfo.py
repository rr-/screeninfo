import importlib
import typing as T

from screeninfo.common import Enumerator, Monitor, ScreenInfoError

_ENUMERATOR_TO_MODULE_PATH = {
    Enumerator.Windows: "screeninfo.enumerators.windows",
    Enumerator.Cygwin: "screeninfo.enumerators.cygwin",
    Enumerator.X11: "screeninfo.enumerators.x11",
    Enumerator.DRM: "screeninfo.enumerators.drm",
    Enumerator.OSX: "screeninfo.enumerators.osx",
}


def _get_monitors(enumerator_module_path: str) -> T.List[Monitor]:
    module = importlib.import_module(enumerator_module_path)
    return list(module.enumerate_monitors())


def get_monitors(name: T.Optional[Enumerator] = None) -> T.List[Monitor]:
    enumerator = Enumerator(name) if name is not None else None

    """Returns a list of :class:`Monitor` objects based on active monitors."""
    if enumerator is not None:
        if enumerator not in _ENUMERATOR_TO_MODULE_PATH:
            raise ScreenInfoError("Unknown enumerator: " + enumerator.value)

        return _get_monitors(_ENUMERATOR_TO_MODULE_PATH[enumerator])

    for module_path in _ENUMERATOR_TO_MODULE_PATH.values():
        try:
            return _get_monitors(module_path)
        except Exception:
            pass
    raise ScreenInfoError("No enumerators available")
