from config.pygame_setup import pygame
import game


class Main():
    """Main entry point to initialize and run the game."""

    def __init__(self):
        """Creates game instance."""
        self.game = game.Game()
        self.running_game = True

    def run_game(self):
        """Method to run game loop, handling music and Pygame shutdown."""
        pygame.mixer.music.play(-1)
        while self.running_game:
            self.running_game = self.game.game_loop()
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        pygame.quit()


main = Main()
main.run_game()
