import pygame
from textwrap import wrap

from draw_text import DrawText
from object import Object
from global_vars import color_dark, font


class HelperDialogue(pygame.sprite.DirtySprite, Object, DrawText):
    """Helper with speechbubble giving useful tips."""

    def __init__(self, x, y):
        """Create the helper, speechbubble and needed data."""
        pygame.sprite.DirtySprite.__init__(self)
        Object.__init__(self, x, y)
        self.dirty = 2
        self._helper_image = pygame.image.load(
            "assets/helper.png").convert_alpha()
        self._speech_bubble_image = pygame.image.load(
            "assets/speech_bubble.png").convert_alpha()

        backgroung_surface = pygame.Surface((1100, 150), pygame.SRCALPHA)
        backgroung_surface.blit(self._helper_image, (0, 0))
        backgroung_surface.blit(self._speech_bubble_image, (100, 0))

        self.image = backgroung_surface
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self._level_text_lines = []
        self._level_line_max = 0
        self._level_line_index = 0

        self._error_text_lines = [
            ["Automaton is deterministic, that means it can have only one state with the same letter."],
            ["Automaton is deterministic, it cannot have more than one initial state."],
            ["Automaton must have at least one initial state."],
            ["All states must have at least one symbol."]
        ]

    @property
    def level_line_index(self):
        return self._level_line_index
    
    @level_line_index.setter
    def level_line_index(self, new_value):
        self._level_line_index = new_value

    def initialize_level_dialogue(self, info):
        """Initialises the dialogue from the level info."""
        self._level_text_lines = info.text_lines
        # avoiding one off mistake, lines are indexed from 0
        self._level_line_max = len(self._level_text_lines) - 1
        # avoiding one off mistake, draw automaton text advances the index each time called, so initialising at one less
        self._level_line_index = - 1

    def draw_automaton_text(self, automaton_response):
        """Displays interpreted data returned from the automaton."""
        text_lines = None
        line_index = 0  # there is only one line in the chosen text

        # choosing text for speech bubble based on automaton response
        if automaton_response is True:
            text_lines = ["Automaton is correct! Press enter to continue."]
        elif isinstance(automaton_response, tuple):
            if automaton_response[1]:
                text_lines = [
                    f"Automaton should accept \"{automaton_response[0]}\" but doesnt."]
            else:
                text_lines = [
                    f"Automaton shouldn't accept \"{automaton_response[0]}\" but does."]
        elif isinstance(automaton_response, int):
            text_lines = self._error_text_lines[automaton_response]
        # cant have just else -> it will overdraw the dialogue that helper is supposed to make

        if text_lines:
            self._draw_text_lines(text_lines, line_index)

    def draw_level_text(self):
        # if already at the end of tips, and presing enter, remain at the last line
        if self._level_line_index < self._level_line_max:
            self._level_line_index += 1

        self._draw_text_lines(self._level_text_lines, self._level_line_index)

    def _draw_text_lines(self, text, line_index):
        """Draws line of text. If the line is too long, it gets split up to fit the speech bubble."""
        # wiping clean and drawing background again, so the old text doesnt persist
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self._helper_image, (0, 0))
        self.image.blit(self._speech_bubble_image, (100, 0))

        current_text = text[line_index]
        # splitting text without splitting word from: https://stackoverflow.com/questions/56653871/split-string-every-n-characters-but-without-splitting-a-word/56653996
        max_length = 67
        split_text = wrap(current_text, max_length) if (
            len(current_text) > max_length) else [current_text]

        # adjusting starting point of text
        offset_x = 150
        offset_y = 26
        offset_start = 15

        line_count = len(split_text)
        for i in range(line_count):
            pos_x = offset_x
            pos_y = offset_start + (i * offset_y)
            self.draw_text_left(
                self.image, split_text[i], font, color_dark, pos_x, pos_y)
