screeninfo
----------

[![Build](https://github.com/rr-/screeninfo/actions/workflows/build.yml/badge.svg)](https://github.com/rr-/screeninfo/actions/workflows/build.yml)

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

# Contributing


```sh
git clone https://github.com/rr-/screeninfo.git # clone this repo
cd screeninfo
poetry install # to install the local venv
poetry run pre-commit install # to setup pre-commit hooks
poetry shell # to enter the venv
```

This project uses [poetry](https://python-poetry.org/) for packaging,
install instructions at [poetry#installation](https://python-poetry.org/docs/#installation)
