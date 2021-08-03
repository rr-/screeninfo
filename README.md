screeninfo
----------

Fetch location and size of physical screens.

### Supported environments

- MS Windows
- MS Windows: Cygwin
- GNU/Linux: X11 (through Xinerama)
- GNU/Linux: DRM (experimental)
- OSX: (through AppKit)

I don't plan on testing OSX or other environments myself. For this reason,
I strongly encourage pull requests.

### Installation

```
pip install screeninfo
```

If you install it from sources:

```
python3 setup.py install
```

### Usage

```python
from screeninfo import get_monitors
for m in get_monitors():
    print(str(m))
```

**Output**:

```python console
Monitor(x=3840, y=0, width=3840, height=2160, width_mm=1420, height_mm=800, name='HDMI-0', is_primary=False)
Monitor(x=0, y=0, width=3840, height=2160, width_mm=708, height_mm=399, name='DP-0', is_primary=True)
```

### Forcing environment

In some cases (emulating X server on Cygwin etc.) you might want to specify the
driver directly. You can do so by passing extra parameter to `get_monitors()`
like this:

```python
from screeninfo import get_monitors, Enumerator
for m in get_monitors(Enumerator.OSX):
    print(str(m))
```

Available drivers: `windows`, `cygwin`, `x11`, `osx`.
