import pygame

from objects.object import Object


class CircleDestroyer(pygame.sprite.DirtySprite, Object):
    """Circle that destroys circles."""

    def __init__(self, x, y):
        """Creates initialised circle destroyer at a given position."""
        pygame.sprite.DirtySprite.__init__(self)
        Object.__init__(self, x, y)
        self.dirty = 2
        self.image = pygame.image.load(
            "assets/circle_destroyer.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.circle_delete = pygame.mixer.Sound("sounds/circle_delete.mp3")

    def handle_destroying_circle(self, player_group, arrow_group, automaton):
        """Kills the circle being carried by the player."""
        # checking collision with destroyer, so that circles get only deleted when player is standing on it
        player_collision = pygame.sprite.spritecollide(
            self, player_group, False, pygame.sprite.collide_mask)

        target_circle = player_group.sprite.carrying_circle

        # initializing circle_arrows to ensure it is defined before next checks
        circle_arrows = None
        if target_circle:
            circle_arrows = pygame.sprite.spritecollide(
                target_circle, arrow_group, False, pygame.sprite.collide_mask)

            # checking if the circle doesnt have arrows connected to it
            if player_collision and (not circle_arrows):
                # remove from automaton if its like initial, ending, initial_ending
                self._handle_circle_variants(target_circle, automaton)
                # clearning the reference from player
                player_group.sprite.carrying_circle = None
                # removes circle from all groups
                target_circle.kill()
                pygame.mixer.Channel(1).play(self.circle_delete)

    def _handle_circle_variants(self, circle, automaton):
        """Removes the circle variant from the automaton"""
        if circle.variant == "initial":
            automaton.remove_initial_state(circle.number)
        elif circle.variant == "accepting":
            automaton.remove_accepting_state(circle.number)
        elif circle.variant == "initial_accepting":
            automaton.remove_initial_state(circle.number)
            automaton.remove_accepting_state(circle.number)
