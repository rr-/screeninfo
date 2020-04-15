
import typing as T
import ctypes
import ctypes.wintypes
from ctypes.wintypes import (
    HMONITOR,
    HDC,
    LPARAM,
    LPRECT,
    WCHAR,
    DWORD,
    RECT,
    BOOL, HWND,
)

from screeninfo.common import Monitor


def enumerate_monitors() -> T.Iterable[Monitor]:

    CCHDEVICENAME = 32
    # gdi32.GetDeviceCaps keys for monitor size in mm
    HORZSIZE = 4
    VERTSIZE = 6

    # https://docs.microsoft.com/en-gb/windows/win32/api/winuser/ns-winuser-monitorinfoexw
    class MONITORINFOEXW(ctypes.Structure):
        _fields_ = [
            ("cbSize", DWORD),
            ("rcMonitor", RECT),
            ("rcWork", RECT),
            ("dwFlags", DWORD),
            ("szDevice", WCHAR * CCHDEVICENAME),
        ]

    LPMONITORINFO = ctypes.POINTER(MONITORINFOEXW)
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmonitorinfow
    GetMonitorInfoW = ctypes.windll.user32.GetMonitorInfoW
    GetMonitorInfoW.restype = BOOL
    GetMonitorInfoW.argtypes = (HMONITOR, LPMONITORINFO)

    # https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getdevicecaps
    GetDeviceCaps = ctypes.windll.gdi32.GetDeviceCaps
    GetDeviceCaps.restype = ctypes.c_int
    GetDeviceCaps.argtype = (HDC, ctypes.c_int)

    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdc
    GetDC = ctypes.windll.user32.GetDC
    GetDC.restype = HDC
    GetDC.argtype = (HWND, )

    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-releasedc
    ReleaseDC = ctypes.windll.user32.ReleaseDC
    ReleaseDC.restype = ctypes.c_int
    ReleaseDC.argtype = (HWND, HDC)

    # https://docs.microsoft.com/en-gb/windows/win32/api/winuser/nc-winuser-monitorenumproc
    MonitorEnumProc = ctypes.WINFUNCTYPE(
        BOOL,  # resType
        HMONITOR,  # monitor
        HDC,  # dc
        LPRECT,  # rect
        LPARAM,  # data
    )

    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaymonitors
    EnumDisplayMonitors = ctypes.windll.user32.EnumDisplayMonitors
    EnumDisplayMonitors.restype = BOOL
    EnumDisplayMonitors.argtype = (HDC, LPRECT, MonitorEnumProc, LPARAM)

    monitors = []

    def callback(monitor: T.Any, dc: T.Any, rect: T.Any, data: T.Any) -> int:
        info = MONITORINFOEXW()
        info.cbSize = ctypes.sizeof(MONITORINFOEXW)
        if GetMonitorInfoW(monitor, ctypes.byref(info)):
            name = info.szDevice
        else:
            name = None

        h_size = GetDeviceCaps(dc, HORZSIZE)
        v_size = GetDeviceCaps(dc, VERTSIZE)

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
    #
    # benshep 2020-03-31: this gives the correct behaviour on Windows 10 when
    # multiple monitors have different DPIs.
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    hwnd = HWND(None)
    # On Python 3.8.X GetDC randomly fails returning an invalid DC.
    # To workaround this request a number of DCs until a valid DC is returned.
    for retry in range(100):
        # Create a Device Context for the full virtual desktop.
        # On failure, GetDC returns NULL
        dc_full: HDC = GetDC(hwnd)
        if dc_full is not None:
            # Got a valid DC, break.
            break
        ReleaseDC(hwnd, dc_full)
    else:
        # Fallback to device context 0 that is the whole
        # desktop. This allows fetching resolutions
        # but monitor specific device contexts are not
        # passed to the callback which means that physical
        # sizes can't be read.
        dc_full = HDC(None)
    # Call EnumDisplayMonitors with the non-NULL DC
    # so that non-NULL DCs are passed onto the callback.
    # We want monitor specific DCs in the callback.

    EnumDisplayMonitors(
        dc_full,
        LPRECT(None),
        # Make sure you keep references to CFUNCTYPE() or WINFUNCTYPE() objects as long as they are
        # used from C code. ctypes doesn’t, and if you don’t, they may be garbage collected,
        # crashing your program when a callback is made.
        MonitorEnumProc(callback),
        LPARAM(0)
    )
    ReleaseDC(hwnd, dc_full)

    yield from monitors
