import ctypes
import ctypes.wintypes
import typing as T

from screeninfo.common import Monitor

CCHDEVICENAME = 32

MonitorEnumProc = ctypes.WINFUNCTYPE(
    ctypes.c_int,
    ctypes.c_ulong,
    ctypes.c_ulong,
    ctypes.POINTER(ctypes.wintypes.RECT),
    ctypes.c_double,
)


class MONITORINFOEXW(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.wintypes.DWORD),
        ("rcMonitor", ctypes.wintypes.RECT),
        ("rcWork", ctypes.wintypes.RECT),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("szDevice", ctypes.wintypes.WCHAR * CCHDEVICENAME),
    ]


def enumerate_monitors() -> T.Iterable[Monitor]:
    monitors = []

    def callback(monitor: T.Any, dc: T.Any, rect: T.Any, data: T.Any) -> int:
        info = MONITORINFOEXW()
        info.cbSize = ctypes.sizeof(MONITORINFOEXW)
        if ctypes.windll.user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
            name = info.szDevice
        else:
            name = None

        rct = rect.contents
        monitors.append(
            Monitor(
                x=rct.left,
                y=rct.top,
                width=rct.right - rct.left,
                height=rct.bottom - rct.top,
                name=name,
            )
        )
        return 1

    ctypes.windll.user32.EnumDisplayMonitors(
        0, 0, MonitorEnumProc(callback), 0
    )

    yield from monitors
