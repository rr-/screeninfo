"""
Author: Marcin Kurczewski and others
License: MIT License
Copyright (C) 2015 Marcin Kurczewski
"""
import ctypes
import ctypes.util


def load_library(name):
    """Load a ctypes library and provide error handling"""
    path = ctypes.util.find_library(name)
    if not path:
        return None
    library = ctypes.cdll.LoadLibrary(path)
    # library can be None
    return library
