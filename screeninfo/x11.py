"""
Author: Marcin Kurczewski and others
License: MIT License
Copyright (C) 2015 Marcin Kurczewski
"""
from .monitor import Monitor
from .utils import load_library


def enumerate_x11():
    """
    Create a list of Monitor instances for any platform running X11 with
    the Xinerama library enabled.
    """
    import ctypes.util

    class XineramaScreenInfo(ctypes.Structure):
        _fields_ = [
            ('screen_number', ctypes.c_int),
            ('x', ctypes.c_short),
            ('y', ctypes.c_short),
            ('width', ctypes.c_short),
            ('height', ctypes.c_short),
        ]

    xlib = load_library('X11')
    xlib.XOpenDisplay.argtypes = [ctypes.c_char_p]
    xlib.XOpenDisplay.restype = ctypes.POINTER(ctypes.c_void_p)
    d = xlib.XOpenDisplay(b'')
    if d is None:
        raise Exception('Could not open X11 display')

    xinerama = load_library('Xinerama')

    number = ctypes.c_int()
    xinerama.XineramaQueryScreens.restype = (
        ctypes.POINTER(XineramaScreenInfo))
    infos = xinerama.XineramaQueryScreens(d, ctypes.byref(number))
    infos = ctypes.cast(
        infos, ctypes.POINTER(XineramaScreenInfo * number.value)).contents

    return [Monitor(i.x, i.y, i.width, i.height) for i in infos]
