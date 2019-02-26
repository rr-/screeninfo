import ctypes
import ctypes.util
import typing as T

from screeninfo.common import Monitor, ScreenInfoError


def load_library(name: str) -> T.Any:
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


def enumerate_monitors() -> T.Iterable[Monitor]:
    xlib = load_library("X11")
    xlib.XOpenDisplay.argtypes = [ctypes.c_char_p]
    xlib.XOpenDisplay.restype = ctypes.POINTER(ctypes.c_void_p)
    display = xlib.XOpenDisplay(b"")
    if not display:
        raise ScreenInfoError("Could not open display")

    try:
        xinerama = load_library("Xinerama")
        if not xinerama.XineramaIsActive(display):
            raise ScreenInfoError("Xinerama is not active")

        number = ctypes.c_int()
        xinerama.XineramaQueryScreens.restype = ctypes.POINTER(
            XineramaScreenInfo
        )
        infos = xinerama.XineramaQueryScreens(display, ctypes.byref(number))
        infos = ctypes.cast(
            infos, ctypes.POINTER(XineramaScreenInfo * number.value)
        ).contents

        for info in infos:
            yield Monitor(
                x=info.x, y=info.y, width=info.width, height=info.height
            )

    finally:
        xlib.XCloseDisplay.restype = ctypes.POINTER(ctypes.c_void_p)
        xlib.XCloseDisplay(display)
