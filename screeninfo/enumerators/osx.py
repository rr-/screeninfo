import typing as T

from screeninfo.common import Monitor


# https://developer.apple.com/documentation/appkit/nsscreen/1388371-main
# first entry in array is always the primary screen
def check_primary(screens: T.Any, screen: T.Any) -> bool:
    return screen == screens[0]


def enumerate_monitors() -> T.Iterable[Monitor]:
    from AppKit import NSScreen, NSDeviceSize
    from Quartz import CGDisplayScreenSize

    screens = NSScreen.screens()

    for screen in screens:
        f = screen.frame
        if callable(f):
            f = f()

        description = screen.deviceDescription()
        width, height = description[NSDeviceSize].sizeValue()
        width_mm, height_mm = CGDisplayScreenSize(description["NSScreenNumber"])
        yield Monitor(
            x=int(f.origin.x),
            y=int(f.origin.y),
            width=width,
            height=height,
            scale=screen.backingScaleFactor(),
            width_mm=width_mm,
            height_mm=height_mm,
            is_primary=check_primary(screens, screen),
        )
