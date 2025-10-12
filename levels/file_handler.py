from levels.level import Level
from levels.save import Save


class FileHandler():
    """Handles json files of levels and saves."""

    def __init__(self):
        """Creates file handler and initialises save data."""
        # both game class and menu class accesses the save, they are both working with one save -> made it an attribute
        self._max_det_levels = 4
        self._max_nondet_levels = 4
        self.save = Save(self._max_det_levels, self._max_nondet_levels)

    def load_level(self, section, level):
        """Initialises level at the given section and level number."""
        level = Level(section, level)
        level.initialize_data()
        return level

    def load_unlocks(self):
        """Loads the unlocked levels."""
        self.save.load_data()
        return self.save

    def save_unlocked_level(self, section, level):
        """Saves that the given level is unlocked."""
        self.save.save_unlocked_level(section, level)
