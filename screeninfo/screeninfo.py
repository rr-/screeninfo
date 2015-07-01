import os
import sys

class Monitor(object):
    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return 'monitor(%dx%d+%d+%d)' % (
            self.width, self.height, self.x, self.y)

class MonitorEnumeratorWindows(object):
    @staticmethod
    def detect():
        return 'cygwin' in sys.platform

    @staticmethod
    def get_monitors():
        import json
        import subprocess
        ps_cmd = [
            'Add-Type -AssemblyName System.Windows.Forms',
            '[System.Windows.Forms.Screen]::AllScreens|ConvertTo-Json'
        ]
        ps = subprocess.Popen(
            ['powershell', '-command', ';'.join(ps_cmd)],
            stdout=subprocess.PIPE)
        output = ps.stdout.read().decode('utf-8')
        bounds = [m['Bounds'] for m in json.loads(output)]
        return [
            Monitor(b['X'], b['Y'], b['Width'], b['Height']) for b in bounds]

class MonitorEnumeratorX11(object):
    @staticmethod
    def detect():
        return 'DISPLAY' in os.environ

    @staticmethod
    def get_monitors():
        import ctypes
        import ctypes.util

        def load_library(name):
            path = ctypes.util.find_library(name)
            if not path:
                raise ImportError('Could not load ' + name)
            return ctypes.cdll.LoadLibrary(path)

        class XineramaScreenInfo(ctypes.Structure):
            _fields_ = [
                ('screen_number', ctypes.c_int),
                ('x', ctypes.c_short),
                ('y', ctypes.c_short),
                ('width', ctypes.c_short),
                ('height', ctypes.c_short),
            ]

        xlib = load_library('X11')
        xlib.XOpenDisplay.argtypes = [ctypes.c_char_p]
        xlib.XOpenDisplay.restype = ctypes.POINTER(ctypes.c_void_p)
        d = xlib.XOpenDisplay(b'')
        if not d:
            raise Exception('Could not open display')

        xinerama = load_library('Xinerama')
        if not xinerama.XineramaIsActive(d):
            raise Exception('Xinerama is not active')

        number = ctypes.c_int()
        xinerama.XineramaQueryScreens.restype = (
            ctypes.POINTER(XineramaScreenInfo))
        infos = xinerama.XineramaQueryScreens(d, ctypes.byref(number))
        infos = ctypes.cast(
            infos, ctypes.POINTER(XineramaScreenInfo * number.value)).contents

        return [Monitor(i.x, i.y, i.width, i.height) for i in infos]

def get_monitors():
    enumerators = [MonitorEnumeratorWindows, MonitorEnumeratorX11]
    for e in enumerators:
        if e.detect():
            chosen = e
    if chosen is None:
        raise NotImplementedError('This environment is not supported.')
    return chosen.get_monitors()

if __name__ == '__main__':
    for m in get_monitors():
        print(str(m))
