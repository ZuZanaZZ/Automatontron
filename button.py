import pygame

from button_variant import PressedVariant, UnpressedVariant
from object import Object


class Button(pygame.sprite.DirtySprite, Object):
    """Button with pressed and unpressed variants."""

    def __init__(self, x, y):
        """Creates and houses the variant of the button."""
        pygame.sprite.DirtySprite.__init__(self)
        Object.__init__(self, x, y)
        self.dirty = 2
        # strategy design pattern https://www.youtube.com/watch?v=WQ8bNdxREHU&t
        self.variant_var = UnpressedVariant(self)

        self.automaton_accepts = pygame.mixer.Sound("sounds/automaton_accepts.mp3")
        self.automaton_rejects = pygame.mixer.Sound("sounds/automaton_rejects.mp3")

    def switch_variant(self, new_variant):
        """Switches variant of the arrow according to the selected new variant."""
        match new_variant:
            case "pressed":
                self.variant_var = PressedVariant(self)
            case "unpressed":
                self.variant_var = UnpressedVariant(self)

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

    def button_pressed(self, player_automaton, level_automaton):
        """Calls the variant's method with both automata."""
        automaton_response = self.variant_var.button_pressed(player_automaton, level_automaton)

        if automaton_response is True:
            pygame.mixer.Channel(1).play(self.automaton_accepts)
        else:
            pygame.mixer.Channel(1).play(self.automaton_rejects)

        return automaton_response