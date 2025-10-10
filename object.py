class Object():
    """Object with coordinates."""

    def __init__(self, x, y):
        """Creates the object on the given coordinates."""
        self.x = x
        self.y = y

    def position_update(self, new_x, new_y, rect):
        """Updates the positionn of the object to the new coordinates."""
        self.x = new_x
        self.y = new_y
        rect.center = (self.x, self.y)
