import os
import sys

class Monitor(object):
    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return 'monitor(%dx%d+%d+%d)' % (
            self.width, self.height, self.x, self.y)

class MonitorEnumeratorWindows(object):
    @staticmethod
    def detect():
        return 'win32' in sys.platform

    @staticmethod
    def get_monitors():
        import ctypes
        import ctypes.wintypes
        monitors = []

        def callback(monitor, dc, rect, data):
            rct = rect.contents
            monitors.append(Monitor(
                rct.left,
                rct.top,
                rct.right - rct.left,
                rct.bottom - rct.top))
            return 1

        MonitorEnumProc = ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_ulong,
            ctypes.c_ulong,
            ctypes.POINTER(ctypes.wintypes.RECT),
            ctypes.c_double)

        ctypes.windll.user32.EnumDisplayMonitors(
            0, 0, MonitorEnumProc(callback), 0)

        return monitors

class MonitorEnumeratorCygwin(object):
    @staticmethod
    def detect():
        return 'cygwin' in sys.platform

    @staticmethod
    def get_monitors():
        import ctypes
        user32 = ctypes.cdll.LoadLibrary('user32.dll')

        LONG = ctypes.c_int32
        BOOL = ctypes.c_int
        HANDLE = ctypes.c_void_p
        HMONITOR = HANDLE
        HDC = HANDLE
        if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
            WPARAM = ctypes.c_ulong
            LPARAM = ctypes.c_long
        elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
            WPARAM = ctypes.c_ulonglong
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

        def callback(monitor, dc, rect, data):
            rct = rect.contents
            monitors.append(Monitor(
                rct.left,
                rct.top,
                rct.right - rct.left,
                rct.bottom - rct.top))
            return 1

        user32.EnumDisplayMonitors(None, None, MonitorEnumProc(callback), 0)
        return monitors

class MonitorEnumeratorX11(object):
    @staticmethod
    def detect():
        return 'DISPLAY' in os.environ

    @staticmethod
    def get_monitors():
        import ctypes
        import ctypes.util

        def load_library(name):
            path = ctypes.util.find_library(name)
            if not path:
                raise ImportError('Could not load ' + name)
            return ctypes.cdll.LoadLibrary(path)

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
        if not d:
            raise Exception('Could not open display')

        xinerama = load_library('Xinerama')
        if not xinerama.XineramaIsActive(d):
            raise Exception('Xinerama is not active')

        number = ctypes.c_int()
        xinerama.XineramaQueryScreens.restype = (
            ctypes.POINTER(XineramaScreenInfo))
        infos = xinerama.XineramaQueryScreens(d, ctypes.byref(number))
        infos = ctypes.cast(
            infos, ctypes.POINTER(XineramaScreenInfo * number.value)).contents

        return [Monitor(i.x, i.y, i.width, i.height) for i in infos]

def get_monitors():
    enumerators = [
        MonitorEnumeratorWindows,
        MonitorEnumeratorCygwin,
        MonitorEnumeratorX11]
    chosen = None
    for e in enumerators:
        if e.detect():
            chosen = e
    if chosen is None:
        raise NotImplementedError('This environment is not supported.')
    return chosen.get_monitors()

if __name__ == '__main__':
    for m in get_monitors():
        print(str(m))
