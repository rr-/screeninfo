from setuptools import setup

setup(
    name="screeninfo",
    packages=["screeninfo", "screeninfo.enumerators"],
    version="0.6.6",
    description="Fetch location and size of physical screens.",
    author="rr-",
    author_email="rr-@sakuya.pl",
    url="https://github.com/rr-/screeninfo",
    keywords=["screen", "monitor", "desktop"],
    classifiers=[],
    install_requires=[
        "dataclasses ; python_version<'3.7'",
        'Cython ; sys_platform=="darwin"',
        'pyobjus ; sys_platform=="darwin"',
    ],
)
