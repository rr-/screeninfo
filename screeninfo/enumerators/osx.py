import typing as T

from pyobjus import autoclass
from pyobjus.dylib_manager import INCLUDE, load_framework
from screeninfo.common import Monitor


def enumerate_monitors() -> T.Iterable[Monitor]:
    load_framework(INCLUDE.AppKit)

    screens = autoclass("NSScreen").screens()

    for i in range(screens.count()):
        f = screens.objectAtIndex_(i).frame
        if callable(f):
            f = f()

        yield Monitor(
            x=f.origin.x,
            y=f.origin.y,
            width=f.size.width,
            height=f.size.height,
        )
