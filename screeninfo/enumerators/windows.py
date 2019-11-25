import typing as T

from screeninfo.common import Monitor


def enumerate_monitors() -> T.Iterable[Monitor]:
    import ctypes
    import ctypes.wintypes

    CCHDEVICENAME = 32
    # gdi32.GetDeviceCaps keys for monitor size in mm
    HORZSIZE = 4
    VERTSIZE = 6

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

    monitors = []

    def callback(monitor: T.Any, dc: T.Any, rect: T.Any, data: T.Any) -> int:
        info = MONITORINFOEXW()
        info.cbSize = ctypes.sizeof(MONITORINFOEXW)
        if ctypes.windll.user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
            name = info.szDevice
        else:
            name = None

        h_size = ctypes.windll.gdi32.GetDeviceCaps(dc, HORZSIZE)
        v_size = ctypes.windll.gdi32.GetDeviceCaps(dc, VERTSIZE)

        rct = rect.contents
        monitors.append(
            Monitor(
                x=rct.left,
                y=rct.top,
                width=rct.right - rct.left,
                height=rct.bottom - rct.top,
                width_mm=h_size,
                height_mm=v_size,
                name=name,
            )
        )
        return 1

    # Make the process DPI aware so it will detect the actual
    # resolution and not a virtualized resolution reported by
    # Windows when DPI virtualization is in use.
    ctypes.windll.user32.SetProcessDPIAware()
    # Create a Device Context for the full virtual desktop.
    dc_full = ctypes.windll.user32.GetDC(None)
    # Call EnumDisplayMonitors with the non-NULL DC
    # so that non-NULL DCs are passed onto the callback.
    # We want monitor specific DCs in the callback.
    ctypes.windll.user32.EnumDisplayMonitors(
        dc_full, None, MonitorEnumProc(callback), 0
    )

    yield from monitors
