class DrawText():
    """Mix in class for drawing text on a surface"""

    def draw_text(self, image, text, font, color, x, y):
        """Draws text at the  given coordinates."""
        text = font.render(text, True, color)  # making text into image
        # making the midbottom of text rectangle to be on the given position
        text_rect = text.get_rect(midbottom=(x, y))
        # drawing text image image, at text_rect position
        image.blit(text, text_rect)

    def draw_text_left(self, image, text, font, color, x, y):
        """Draws text justified to left at the given coordinates."""
        text = font.render(text, True, color)
        text_rect = text.get_rect(topleft=(x, y))
        image.blit(text, text_rect)

    def draw_text_centered(self, image, text, font, color):
        """Draws text centered on the given image."""
        text = font.render(text, True, color)
        text_rect = text.get_rect(center=image.get_rect().center)
        image.blit(text, text_rect)
