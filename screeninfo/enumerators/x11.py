import ctypes
import ctypes.util

from screeninfo.common import Monitor, ScreenInfoError


def load_library(name):
    path = ctypes.util.find_library(name)
    if not path:
        raise ScreenInfoError("Could not load " + name)
    return ctypes.cdll.LoadLibrary(path)


class XineramaScreenInfo(ctypes.Structure):
    _fields_ = [
        ("screen_number", ctypes.c_int),
        ("x", ctypes.c_short),
        ("y", ctypes.c_short),
        ("width", ctypes.c_short),
        ("height", ctypes.c_short),
    ]


def enumerate_monitors():
    xlib = load_library("X11")
    xlib.XOpenDisplay.argtypes = [ctypes.c_char_p]
    xlib.XOpenDisplay.restype = ctypes.POINTER(ctypes.c_void_p)
    d = xlib.XOpenDisplay(b"")
    if d:
        try:
            xinerama = load_library("Xinerama")
            if not xinerama.XineramaIsActive(d):
                raise ScreenInfoError("Xinerama is not active")

            number = ctypes.c_int()
            xinerama.XineramaQueryScreens.restype = ctypes.POINTER(
                XineramaScreenInfo
            )
            infos = xinerama.XineramaQueryScreens(d, ctypes.byref(number))
            infos = ctypes.cast(
                infos, ctypes.POINTER(XineramaScreenInfo * number.value)
            ).contents

            ans = [Monitor(i.x, i.y, i.width, i.height) for i in infos]
        finally:
            xlib.XCloseDisplay.restype = ctypes.POINTER(ctypes.c_void_p)
            xlib.XCloseDisplay(d)

        return ans
    else:
        raise ScreenInfoError("Could not open display")
