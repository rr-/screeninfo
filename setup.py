from setuptools import setup

# Collect the Current README docs for PyPI
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="screeninfo",
    packages=["screeninfo", "screeninfo.enumerators"],
    version="0.6.6",
    description="Fetch location and size of physical screens.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="rr-",
    author_email="rr-@sakuya.pl",
    url="https://github.com/rr-/screeninfo",
    keywords=["screen", "monitor", "desktop"],
    classifiers=[
        'Operating System :: MacOS :: MacOS X :: PyOBJus',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Cygwin',
        'Operating System :: Linux :: X11',
        'Operating System :: Linux :: DRM :: Experimental'
    ],
    install_requires=[
        "dataclasses ; python_version<'3.7'",
        'Cython ; sys_platform=="darwin"',
        'pyobjus ; sys_platform=="darwin"',
    ],
)
