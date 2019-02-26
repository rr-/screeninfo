import enum
import typing as T
from dataclasses import dataclass


@dataclass
class Monitor:
    """Stores the resolution and position of a monitor."""

    x: int
    y: int
    width: int
    height: int
    name: T.Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"Monitor("
            f"x={self.x}, y={self.y}, "
            f"width={self.width}, height={self.height}, "
            f"name={self.name!r}"
            f")"
        )


class ScreenInfoError(Exception):
    pass


class Enumerator(enum.Enum):
    Windows = "windows"
    Cygwin = "cygwin"
    Xrandr = "xrandr"
    Xinerama = "xinerama"
    DRM = "drm"
    OSX = "osx"
