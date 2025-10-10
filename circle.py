import pygame

from circle_variant import BaseVariant, InitialVariant, AcceptingVariant, InitialAcceptingVariant
from object import Object


class Circle(pygame.sprite.Sprite, Object):
    """Circle with base, accepting, initial and initial accepting variants."""

    def __init__(self, x, y, number):
        """Creates and houses the variant of the circle."""
        pygame.sprite.Sprite.__init__(self)
        Object.__init__(self, x, y)
        self.variant_var = BaseVariant(self, number)

    def switch_variant(self, new_variant):
        """Switches variant of the circle according to the selected new variant."""
        match new_variant:
            case "base":
                self.variant_var = BaseVariant(self, self.number)
            case "initial":
                self.variant_var = InitialVariant(self, self.number)
            case "accepting":
                self.variant_var = AcceptingVariant(self, self.number)
            case "initial_accepting":
                self.variant_var = InitialAcceptingVariant(self, self.number)

    @property
    def number(self):
        return self.variant_var._number

    @property
    def variant(self):
        return self.variant_var._variant

    @property
    def image(self):
        return self.variant_var._image

    @property
    def rect(self):
        return self.variant_var._rect

    @property
    def mask(self):
        return self.variant_var._mask
