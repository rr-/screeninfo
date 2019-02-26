import importlib
import typing as T
from pathlib import Path

from screeninfo.common import Enumerator, Monitor, ScreenInfoError


def _get_monitors(enumerator: Enumerator) -> T.List[Monitor]:
    enumerator_module_path = f"screeninfo.enumerators.{enumerator.value}"
    module = importlib.import_module(enumerator_module_path)
    return list(module.enumerate_monitors())


def get_monitors(
    name: T.Union[Enumerator, str, None] = None
) -> T.List[Monitor]:
    """Returns a list of :class:`Monitor` objects based on active monitors."""
    enumerator = Enumerator(name) if name is not None else None

    if enumerator is not None:
        return _get_monitors(enumerator)

    for enumerator in Enumerator:
        try:
            return _get_monitors(enumerator)
        except Exception:
            pass

    raise ScreenInfoError("No enumerators available")
