import pygame

from objects.circle import Circle
from objects.object import Object


class CircleGenerator(pygame.sprite.DirtySprite, Object):
    """Circle that generates circles."""

    def __init__(self, x, y):
        """Creates initialised circle generator at a given position."""
        pygame.sprite.DirtySprite.__init__(self)
        Object.__init__(self, x, y)
        self.dirty = 2
        self.image = pygame.image.load(
            "assets/circle_generator.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.number = 0
        self._is_disabled = True
        self._player_standing_in = False

        self.circle_create = pygame.mixer.Sound("sounds/circle_create.mp3")

    def reset_count(self):
        self.number = 0

    def enable(self):
        self._is_disabled = False

    def disable(self):
        self._is_disabled = True

    def handle_new_circles(self, player_group, circle_group):
        """Generates a circle, if player is standing on the generator, and doesn't already have a circle."""
        if self._is_disabled:
            return # disables creation of circles during the completion screen
        
        creation_circles = pygame.sprite.spritecollide(
            self, player_group, False, pygame.sprite.collide_mask)

        circles = pygame.sprite.spritecollide(
            player_group.sprite, circle_group, False, pygame.sprite.collide_mask)

        # add new circle if player isnt standing in creation circle already, and if no circles are present
        if creation_circles and (not circles):
            creation_circle = creation_circles[0]
            if creation_circle and not self._player_standing_in:
                circle_group.add(self._add_new_circle())
                self._player_standing_in = True
                pygame.mixer.Channel(1).play(self.circle_create)

        # reset flag
        elif (not creation_circles) and self._player_standing_in:
            self._player_standing_in = False

    def _add_new_circle(self):
        """factory method to create a new Circle instance"""
        y_offset = 35
        new_circle = Circle(self.x, self.y - y_offset, self.number)
        self.number += 1
        return new_circle
