"""
Author: Marcin Kurczewski and others
License: MIT License
Copyright (C) 2015 Marcin Kurczewski
"""


class Monitor(object):
    """
    Monitor class that provides the details of a single monitor.
    """
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
        return 'monitor({}x{}+{}+{})'.format(
            self.width, self.height, self.x, self.y)
