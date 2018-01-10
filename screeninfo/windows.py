"""
Author: Marcin Kurczewski and others
License: MIT License
Copyright (C) 2015 Marcin Kurczewski
"""
from .monitor import Monitor


def enumerate_windows():
    """Create a list of Monitor instances on the Windows platform."""
    import ctypes.wintypes
    monitors = []

    def callback(_monitor, _dc, rect, _data):
        """
        Callback for the ctypes EnumDisplayMonitors win32 function.
        """
        rct = rect.contents
        monitors.append(Monitor(
            rct.left,
            rct.top,
            rct.right - rct.left,
            rct.bottom - rct.top))
        return 1

    monitor_enum_proc = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.POINTER(ctypes.wintypes.RECT),
        ctypes.c_double)

    ctypes.windll.user32.EnumDisplayMonitors(
        0, 0, monitor_enum_proc(callback), 0)

    return monitors
