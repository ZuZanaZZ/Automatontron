import pygame

from abc import ABC


class ButtonVariant(ABC):
    """Describes what attributes should a button variant have."""

    def __init__(self, button):
        """Initialises a blank arrow."""
        self.button = button
        self._variant = None
        self._image = None
        self._rect = None
        self._mask = None


class UnpressedVariant(ButtonVariant):
    """Unpressed variant of the button."""

    def __init__(self, button):
        """Creates and visualises an unpressed variant of the button."""
        super().__init__(button)
        self._variant = "unpressed"
        self._image = pygame.image.load(
            "assets/button_unpressed.png").convert_alpha()
        self._rect = self._image.get_rect(center=(button.x, button.y))
        self._mask = pygame.mask.from_surface(self._image)


class PressedVariant(ButtonVariant):
    """Pressed variant of the button."""

    def __init__(self, button):
        """Creates and visualises a pressed variant of the button."""
        super().__init__(button)
        self._variant = "pressed"
        self._image = pygame.image.load(
            "assets/button_pressed.png").convert_alpha()
        self._rect = self._image.get_rect(center=(button.x, button.y))
        self._mask = pygame.mask.from_surface(self._image)

    def button_pressed(self, player_automaton, level_automaton):
        """Calls the player automaton's method for checking the language equivalence with the level automaton."""
        return player_automaton.handle_checking_language(level_automaton)
