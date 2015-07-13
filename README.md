screeninfo
----------

Fetch location and size of physical screens.

### Supported environments

- MS Windows
- MS Windows: Cygwin
- GNU/Linux: X11 (through Xinerama)

I don't plan on testing OSX or other environments myself. For this reason,
I strongly encourage pull requests.

### Installation

    pip install screeninfo

If you install it from sources:

    python3 setup.py install

### Usage

    from screeninfo import get_monitors
    for m in get_monitors():
        print(str(m))

**Output**:

>monitor(1920x1080+1920+0)  
>monitor(1920x1080+0+0)
