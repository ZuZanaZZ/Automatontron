import pygame

from draw_text import DrawText
from global_vars import screen_height, screen_width, font, font_bold, color_dark, color_light
from menu_variant import MainVariant, LevelVariant, ResolutionVariant, AudioVariant
# basis for menu from: https://www.youtube.com/watch?v=a5JWrd7Y_14&list=PLVFWKkB2K-TnsGDz7xrN27IpCU5I1bery


class Menu(pygame.sprite.Sprite, DrawText):
    """Menu with main, level, resolution and audio variants."""

    def __init__(self, screen):
        """Creates and houses the variant of the menu. Initialises needed variables for opperation."""
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self._running_menu = True
        self.quit_game = False
        self.variant_var = MainVariant(self)

        # fullscreen implementation from: https://stackoverflow.com/questions/31538506/how-do-i-maximize-the-display-screen-in-pygame
        # resizing windows issue: https://github.com/pygame/pygame/issues/4322
        # in here, because if already resized, the values get innacurate
        info = pygame.display.Info()
        self.display_width, self.display_height = info.current_w, info.current_h
        self._new_resolution = None

        self.image = pygame.image.load(
            "assets/menu_background.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (screen_width, screen_height))
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.mask = pygame.mask.from_surface(self.image)

        self.menu_item = pygame.mixer.Sound("sounds/menu_item.mp3")
        self.menu_select = pygame.mixer.Sound("sounds/menu_select.mp3")

        self._key_dict = {
            pygame.K_UP: lambda: self.variant_var.handle_up(),
            pygame.K_DOWN: lambda: self.variant_var.handle_down(),
            pygame.K_ESCAPE: lambda: self.variant_var.handle_esc(),
            pygame.K_RETURN: lambda: self.variant_var.handle_select(),
            pygame.K_SPACE: lambda: self.variant_var.handle_select()
        }

        self._action_dict = {
            "quit game": lambda: self._handle_quit(),
            "game": lambda: self._handle_game(),
            "main": lambda: self._switch_variant("main"),
            "levels": lambda: self._switch_variant("levels"),
            "resolution": lambda: self._switch_variant("resolution"),
            "audio": lambda: self._switch_variant("audio"),
            "1280x720": lambda: self._change_resolution((1280, 720), False),
            "1920x1080": lambda: self._change_resolution((1920, 1080), False),
            "fullscreen": lambda: self._change_resolution((self.display_width, self.display_height), True)
        }

    @property
    def running_menu(self):
        return self._running_menu

    @running_menu.setter
    def running_menu(self, value):
        self._running_menu = value

    @property
    def new_resolution(self):
        return self._new_resolution

    @new_resolution.setter
    def new_resolution(self, value):
        self._new_resolution = value

    @property
    def variant(self):
        return self.variant_var._variant

    @property
    def mode(self):
        return self.variant_var._mode

    @property
    def current_section(self):
        return self.variant_var.current_section

    @property
    def current_level(self):
        return self.variant_var.current_level

    def _switch_variant(self, new_variant):
        """Switches variant of the menu according to the selected new variant."""
        match new_variant:
            case "main":
                self.variant_var = MainVariant(self)
            case "levels":
                self.variant_var = LevelVariant(self)
            case "resolution":
                self.variant_var = ResolutionVariant(self)
            case "audio":
                self.variant_var = AudioVariant(self)

    def menu_loop(self):
        """Loop in which player input and menu events are handled and visualised."""
        while self._running_menu:
            self._handle_input()
            self._handle_drawing()

    def _handle_input(self):
        """Handles the events and input of player."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._handle_quit()
            if event.type == pygame.KEYDOWN:
                self._handle_action(event.key)

    def _handle_quit(self):
        """Sets up for game quitting by adjusting attribute values."""
        self._running_menu = False
        self.quit_game = True

    def _handle_action(self, key):
        """Looks up what action should be done, and performs it."""
        # look up what the key should do
        action = self._key_dict.get(key, lambda: False)()

        # here, so the sound doesnt seem delayed after selection
        if action:
            pygame.mixer.Channel(1).play(self.menu_select)
        else:
            pygame.mixer.Channel(1).play(self.menu_item)


        # if action is requested from menu variants, it is done
        self._action_dict.get(action, lambda: False)()


    def _handle_drawing(self):
        """Visualises the needed menu lines."""
        offset = 75
        width, height = self.screen.get_size()
        menu_items = self.variant_var.modes
        height = height - (len(menu_items) * offset) // 2
        levels_passed = None
        if self.variant == "levels":
            levels_passed = self.variant_var.load_levels()
            for elem in levels_passed:
                elem = not elem

        offset = 50
        for i in range(len(menu_items)):
            save_data = levels_passed[i] if levels_passed else None

            if i == self.variant_var.mode_index:
                position = (width / 2, (height / 2) + i * offset)
                self._selected_item(menu_items[i], position, save_data)
            else:
                position = (width / 2, (height / 2) + i * offset)
                self._deselected_item(menu_items[i], position, save_data)

        pygame.display.flip()  # update display
        self.screen.blit(self.image, (0, 0))  # draw the image on the screen

    def _selected_item(self, state, position, levels_passed):
        """Makes the item be drawn in bold font."""
        used_color = color_light if levels_passed == False else color_dark
        self.draw_text(self.screen, state, font_bold,
                       used_color, position[0], position[1])

    def _deselected_item(self, state, position, levels_passed):
        """Makes the item be drawn in normal font."""
        used_color = color_light if levels_passed == False else color_dark
        self.draw_text(self.screen, state, font,
                       used_color, position[0], position[1])

    # methods related to to the action_dict (called from handle_action)
    def _handle_game(self):
        """Sets up for going into the game on selected by adjusting attribute values."""
        self._running_menu = False

    def _change_resolution(self, new_resolution, fullscreen):
        """Changes the size of the background. Sets up for changing resolution of game by adjusting attribute values"""
        self._new_resolution = new_resolution

        flag = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode(new_resolution, flag)
        self.image = pygame.transform.scale(self.image, new_resolution)

