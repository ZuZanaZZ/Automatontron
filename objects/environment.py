import pygame

from draw_text import DrawText
from config.global_vars import screen_width, screen_height, font, color_light


class Environment(pygame.sprite.Sprite, DrawText):
    """Background of the game, and language of the level automaton."""

    def __init__(self):
        """Creates the background and draws the input language on top."""
        pygame.sprite.Sprite.__init__(self)
        # loading and resizing images upfront, so theres no lag when entering a level
        completion_image = pygame.image.load(
            "assets/completion_background.png").convert_alpha()
        self.completion_image = pygame.transform.scale(
            completion_image, (screen_width, screen_height))
        environment_image = pygame.image.load(
            "assets/environment.png").convert_alpha()
        self.environment_image = pygame.transform.scale(
            environment_image, (screen_width, screen_height))

        self.image = self.environment_image
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.mask = pygame.mask.from_surface(self.image)
        self._input_language = None

    @property
    def input_language(self):
        return self._input_language

    @input_language.setter
    def input_language(self, string):
        self._input_language = string

    def draw_input_language(self, screen):
        """Draws the input language on the bottom of the screen."""
        width, height = screen.get_size()
        x_middle = width / 2
        y_offset = 20

        # redrawing the text every frame, so it stays on the screen
        self.draw_text(screen, self.input_language,
                       font, color_light, x_middle, height - y_offset)

    def change_image(self, new_image):
        """Changes the image of the game's background."""
        if new_image == "environment":
            self.image = self.environment_image
        if new_image == "completion":
            self.image = self.completion_image

    def change_resolution(self, new_resolution):
        """Scale the background image to get to the new resolution."""
        self.image = pygame.transform.scale(self.image, new_resolution)
        self.environment_image = pygame.transform.scale(
            self.environment_image, new_resolution)
        self.completion_image = pygame.transform.scale(
            self.completion_image, new_resolution)
