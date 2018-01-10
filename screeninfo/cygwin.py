"""
Author: Marcin Kurczewski and others
License: MIT License
Copyright (C) 2015 Marcin Kurczewski
"""
from .monitor import Monitor


def enumerate_cygwin():
    """Create a list of Monitor instances on the Cygwin platform."""
    import ctypes
    user32 = ctypes.cdll.LoadLibrary('user32.dll')

    LONG = ctypes.c_int32
    BOOL = ctypes.c_int
    HANDLE = ctypes.c_void_p
    HMONITOR = HANDLE
    HDC = HANDLE

    ptr_size = ctypes.sizeof(ctypes.c_void_p)
    if ptr_size == ctypes.sizeof(ctypes.c_long):
        LPARAM = ctypes.c_long
    else:  # ptr_size == ctypes.sizeof(ctypes.c_longlong):
        LPARAM = ctypes.c_longlong

    class RECT(ctypes.Structure):
        _fields_ = [
            ('left', LONG),
            ('top', LONG),
            ('right', LONG),
            ('bottom', LONG)
        ]

    MonitorEnumProc = ctypes.CFUNCTYPE(
        BOOL,
        HMONITOR,
        HDC,
        ctypes.POINTER(RECT),
        LPARAM)

    user32.EnumDisplayMonitors.argtypes = [
        HANDLE,
        ctypes.POINTER(RECT),
        MonitorEnumProc,
        LPARAM]
    user32.EnumDisplayMonitors.restype = ctypes.c_bool

    monitors = []

    def callback(_monitor, _dc, rect, _data):
        rct = rect.contents
        monitors.append(Monitor(
            rct.left,
            rct.top,
            rct.right - rct.left,
            rct.bottom - rct.top))
        return 1

    user32.EnumDisplayMonitors(None, None, MonitorEnumProc(callback), 0)
    return monitors
