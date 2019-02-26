from pyobjus import autoclass
from pyobjus.dylib_manager import INCLUDE, load_framework
from screeninfo.common import Monitor


def enumerate_monitors():
    load_framework(INCLUDE.AppKit)

    screens = autoclass("NSScreen").screens()

    for i in range(screens.count()):
        f = screens.objectAtIndex_(i).frame
        if callable(f):
            f = f()

        yield Monitor(f.origin.x, f.origin.y, f.size.width, f.size.height)
