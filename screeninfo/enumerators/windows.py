import ctypes
import ctypes.wintypes

from screeninfo.common import Monitor


def enumerate():
    monitors = []

    def callback(_monitor, _dc, rect, _data):
        rct = rect.contents
        monitors.append(
            Monitor(
                rct.left, rct.top, rct.right - rct.left, rct.bottom - rct.top
            )
        )
        return 1

    MonitorEnumProc = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.POINTER(ctypes.wintypes.RECT),
        ctypes.c_double,
    )

    ctypes.windll.user32.EnumDisplayMonitors(
        0, 0, MonitorEnumProc(callback), 0
    )

    return monitors
