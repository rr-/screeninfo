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
    scale: float = 1
    width_mm: T.Optional[int] = None
    height_mm: T.Optional[int] = None
    name: T.Optional[str] = None
    is_primary: T.Optional[bool] = None

    @property
    def ppmm(self) -> T.Optional[T.Tuple[float, float]]:
        if self.width_mm is None or self.height_mm is None:
            return None
        return (self.width/self.width_mm, self.height/self.height_mm)

    def __repr__(self) -> str:
        return (
            f"Monitor("
            f"x={self.x}, y={self.y}, "
            f"width={self.width}, height={self.height}, "
            f"scale={self.scale}, "
            f"width_mm={self.width_mm}, height_mm={self.height_mm}, "
            f"ppmm={self.ppmm!r}, "
            f"name={self.name!r}, "
            f"is_primary={self.is_primary}"
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
