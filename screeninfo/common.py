class Monitor(object):
    """Stores the resolution and position of a monitor."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return "monitor({}x{}+{}+{})".format(
            self.width, self.height, self.x, self.y
        )


class ScreenInfoError(Exception):
    pass
