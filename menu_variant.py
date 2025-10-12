import pygame

from abc import ABC, abstractmethod
from levels.file_handler import FileHandler


class MenuVariant(ABC):
    """Describes what attributes and methods should a menu variant have."""

    def __init__(self, menu):
        """Initialises a blank menu."""
        self.menu = menu
        self._variant = None
        self._image = None
        self._rect = None
        self._mask = None
        self._mode = None

    @abstractmethod
    def handle_up(self):
        pass

    @abstractmethod
    def handle_down(self):
        pass

    @abstractmethod
    def handle_esc(self):
        pass

    @abstractmethod
    def handle_select(self):
        pass


class MainVariant(MenuVariant):
    """Main variant of the menu."""

    def __init__(self, menu):
        """Initialises main variant of the menu."""
        super().__init__(menu)
        self._variant = "main"

        self._mode = "levels"
        self.modes = ["levels", "resolution", "audio", "quit game"]
        self.mode_index = 0

    def handle_up(self):
        """Go up in menu items. If at top, loop to the bottom."""
        self.mode_index = (self.mode_index - 1) % len(self.modes)
        self._mode = self.modes[self.mode_index]

    def handle_down(self):
        """Go down in menu items. If at bottom, loop to the top."""
        self.mode_index = (self.mode_index + 1) % len(self.modes)
        self._mode = self.modes[self.mode_index]

    def handle_esc(self):
        """Return action that should be handled if esc key is pressed."""
        # return "quit" quitting game by pressing esc can be implemented

    def handle_select(self):
        """Switch to the selected menu item."""
        return self._mode  # Switch to the mode of the selected menu item


class LevelVariant(MenuVariant):
    """Level variant of the menu."""

    def __init__(self, menu):
        """Initialises level variant of the menu."""
        super().__init__(menu)
        self._variant = "levels"

        self._mode = "1"
        self.modes = ["deterministic", "1", "2", "3", "4",
                      "nondeterministic", "1", "2", "3", "4"]
        self.mode_index = 1

        self.file_handler = FileHandler()
        self.save_data = self.load_levels()

        self.current_section = None
        self.current_level = None

    def load_levels(self):
        """Loads data on what levels the player unlocked."""
        save = self.file_handler.load_unlocks()
        self.save_data = save.unlocked_levels_data
        return save.unlocked_levels_data

    def handle_up(self):
        """Go up in menu items. If at top, loop to the bottom. If at title of section, skip."""
        if not (self._mode == "1"):
            self.mode_index = (self.mode_index - 1) % len(self.modes)
        else:  # skipping the section names
            self.mode_index = (self.mode_index - 2) % len(self.modes)
        self._mode = self.modes[self.mode_index]

    def handle_down(self):
        """Go down in menu items. If at bottom, loop to the top. If at the title of section, skip."""
        last_level = str((len(self.modes) - 2) // 2)
        if not (self._mode == last_level):
            self.mode_index = (self.mode_index + 1) % len(self.modes)
        else:  # skipping the section names
            self.mode_index = (self.mode_index + 2) % len(self.modes)
        self._mode = self.modes[self.mode_index]

    def handle_esc(self):
        """Return action that should be handled if esc key is pressed."""
        return "main"

    def handle_select(self):
        """Switch to the selected level."""
        # if level is unlocked
        if self.save_data[self.mode_index]:

            level_index = self.mode_index
            level_count_per_section = (len(self.modes)) // 2

            self.current_section = level_index // level_count_per_section
            self.current_level = int(self._mode)

            return "game"


class ResolutionVariant(MenuVariant):
    """Resolution variant of the menu."""

    def __init__(self, menu):
        """Initialises resolution variant of the menu."""
        super().__init__(menu)
        self._variant = "resolution"

        self._mode = "1280x720"
        self.modes = ["1280x720", "1920x1080", "fullscreen"]
        self.mode_index = 0

        # fullscreen implementation from: https://stackoverflow.com/questions/31538506/how-do-i-maximize-the-display-screen-in-pygame
        info = pygame.display.Info()
        self.display_width, self.display_height = info.current_w, info.current_h

    def handle_up(self):
        """Go up in menu items. If at top, loop to the bottom."""
        self.mode_index = (self.mode_index - 1) % len(self.modes)
        self._mode = self.modes[self.mode_index]

    def handle_down(self):
        """Go down in menu items. If at bottom, loop to the top."""
        self.mode_index = (self.mode_index + 1) % len(self.modes)
        self._mode = self.modes[self.mode_index]

    def handle_esc(self):
        """Return to the main menu."""
        return "main"

    def handle_select(self):
        return self._mode  # switch to resolution based on selected item


class AudioVariant(MenuVariant):
    """Audio variant of the menu."""

    def __init__(self, menu):
        """Initialises audio variant of the menu."""
        super().__init__(menu)
        self._variant = "audio"

        self._mode = "music on"
        self.modes = ["music on", "music off", "sound effects on", "sound effects off"]
        self.mode_index = 0

    def handle_up(self):
        """Go up in menu items. If at top, loop to the bottom."""
        self.mode_index = (self.mode_index - 1) % len(self.modes)
        self._mode = self.modes[self.mode_index]

    def handle_down(self):
        """Go down in menu items. If at bottom, loop to the top."""
        self.mode_index = (self.mode_index + 1) % len(self.modes)
        self._mode = self.modes[self.mode_index]

    def handle_esc(self):
        """Return to the main menu."""
        return "main"

    def handle_select(self):
        """Toggles the playing of music and sound effects."""
        if self._mode == "music on":
            pygame.mixer.music.play(-1)
        elif self._mode == "music off":
            pygame.mixer.music.stop()
        # usage of chanels for sound effects from: https://stackoverflow.com/questions/46131369/how-to-stop-sound-in-pygame
        elif self._mode == "sound effects on":
            pygame.mixer.Channel(1).set_volume(1)
        elif self._mode == "sound effects off":
            pygame.mixer.Channel(1).set_volume(0)
