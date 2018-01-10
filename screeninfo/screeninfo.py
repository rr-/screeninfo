"""
Author: Marcin Kurczewski and others
License: MIT License
Copyright (C) 2015 Marcin Kurczewski
"""
from sys import platform
from .cygwin import enumerate_cygwin
from .drm import enumerate_drm
from .osx import enumerate_osx
from .windows import enumerate_windows
from .x11 import enumerate_x11
from .utils import load_library

_ENUMERATORS = {
    'windows': enumerate_windows,
    'cygwin': enumerate_cygwin,
    'x11': enumerate_x11,
    'drm': enumerate_drm,
    'osx': enumerate_osx,
}


def _get_enumerator():
    """
    Perform platform checks and choose the correct enumerator based on
    that platform information.
    """
    if platform == 'win32':
        return enumerate_windows
    elif platform == 'darwin':
        return enumerate_osx
    elif platform == 'cygwin':
        return enumerate_cygwin
    # Linux
    for lib in ('x11', 'drm'):
        try:
            load_library(lib)
        # Does not consider library loading errors
        except FileNotFoundError:
            continue
        return globals()["enumerate_" + lib]
    # If this point in the code is reached, the platform is not one
    # of the supported platforms.
    raise NotImplementedError('This platform is not supported.')


def get_monitors(name=None):
    """
    Return a list of Monitor instances (the result of any enumerator)
    to the user. Uses _get_enumerator to get the appropriate
    enumerator function for the platform.
    """
    enumerator = _ENUMERATORS[name] if name else _get_enumerator()
    return enumerator()


if __name__ == '__main__':
    """
    Example code. Output:
        monitor(1920x1080+1920+0)
        monitor(1920x1080+0+0)
    """
    for m in get_monitors():
        print(str(m))
