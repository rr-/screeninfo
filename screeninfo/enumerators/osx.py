import typing as T

from screeninfo.common import Monitor


def enumerate_monitors() -> T.Iterable[Monitor]:
    from AppKit import NSScreen

    screens = NSScreen.screens()

    for screen in screens:
        f = screen.frame
        if callable(f):
            f = f()

        yield Monitor(
            x=int(f.origin.x),
            y=int(f.origin.y),
            width=int(f.size.width),
            height=int(f.size.height),
        )
