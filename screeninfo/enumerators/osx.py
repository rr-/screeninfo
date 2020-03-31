import typing as T

from screeninfo.common import Monitor


def enumerate_monitors() -> T.Iterable[Monitor]:
    from pyobjus import autoclass
    from pyobjus.dylib_manager import INCLUDE, load_framework

    load_framework(INCLUDE.AppKit)

    screens = autoclass("NSScreen").screens()

    for i in range(screens.count()):
        f = screens.objectAtIndex_(i).frame
        if callable(f):
            f = f()

        yield Monitor(
            x=int(f.origin.x),
            y=int(f.origin.y),
            width=int(f.size.width),
            height=int(f.size.height),
        )
