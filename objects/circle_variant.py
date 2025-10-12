import pygame
from config.global_vars import color_dark, font
from draw_text import DrawText
from abc import ABC


class CircleVariant(ABC, DrawText):
    """Describes what attributes should a circle variant have."""

    def __init__(self, circle, number):
        """Initialises a blank circle."""
        self.circle = circle  # circle is saved to the variable, so there is no duplicate data saved, only accessing circle for position data
        self._number = number
        self._variant = None
        self._image = None
        self._rect = None
        self._mask = None


class BaseVariant(CircleVariant):
    """Base variant of the circle."""

    def __init__(self, circle, number):
        """Creates and visualises a base variant of the circle."""
        super().__init__(circle, number)
        self._variant = "base"
        # load image #making image the desired size
        self._image = pygame.image.load(
            "assets/circle_base.png").convert_alpha()
        # variable called rect is needed for sprite group drawing
        self._rect = self._image.get_rect(
            center=(self.circle.x, self.circle.y))
        self.draw_text_centered(self._image, str(
            self._number), font, color_dark)
        self._mask = pygame.mask.from_surface(self._image)


class InitialVariant(CircleVariant):
    """Initial variant of the circle."""

    def __init__(self, circle, number):
        """Creates and visualises an initial variant of the circle."""
        super().__init__(circle, number)
        self._variant = "initial"

        self._image = pygame.image.load(
            "assets/circle_initial.png").convert_alpha()
        self._rect = self._image.get_rect(
            center=(self.circle.x, self.circle.y))
        self.draw_text_centered(self._image, str(
            self._number), font, color_dark)
        self._mask = pygame.mask.from_surface(self._image)


class AcceptingVariant(CircleVariant):
    """Accepting variant of the circle."""

    def __init__(self, circle, number):
        """Creates and visualises an accepting variant of the circle."""
        super().__init__(circle, number)
        self._variant = "accepting"

        self._image = pygame.image.load(
            "assets/circle_accepting.png").convert_alpha()
        self._rect = self._image.get_rect(
            center=(self.circle.x, self.circle.y))
        self.draw_text_centered(self._image, str(
            self._number), font, color_dark)
        self._mask = pygame.mask.from_surface(self._image)


class InitialAcceptingVariant(CircleVariant):
    """Initial and accepting variant of the circle."""

    def __init__(self, circle, number):
        """Creates and visualises an initial accepting variant of the circle."""
        super().__init__(circle, number)
        self._variant = "initial_accepting"

        self._image = pygame.image.load(
            "assets/circle_initial_accepting.png").convert_alpha()
        self._rect = self._image.get_rect(
            center=(self.circle.x, self.circle.y))
        self.draw_text_centered(self._image, str(
            self._number), font, color_dark)
        self._mask = pygame.mask.from_surface(self._image)
