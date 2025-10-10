import pygame
from automaton import Automaton
from button import Button
from circle_destroyer import CircleDestroyer
from circle_generator import CircleGenerator
from environment import Environment
from file_handler import FileHandler
from global_vars import screen_width, screen_height
from helper_dialogue import HelperDialogue
from menu import Menu
from player import Player


class Game():
    """Main game logic with all core components."""

    def __init__(self):
        """Initialises all needed classes, flags and variables to run the game."""
        self.playing = False
        self._FPS = 60
        self._clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self._screen_width, self._screen_height = self.screen.get_size()

        self._small_offset = 100
        self._medium_offset = 150
        self._big_offset = 200
        middle_of_screen = self._screen_width / 2

        # inicialisation idea from: https://gamedev.stackexchange.com/questions/47723/when-to-use-pygame-sprite-groupsingle
        self.environment_group = pygame.sprite.GroupSingle(Environment())
        # using group for collision, drawing
        self.player_group = pygame.sprite.GroupSingle(
            Player(self._small_offset, self._screen_height - self._big_offset))
        self.button_group = pygame.sprite.GroupSingle(
            Button(middle_of_screen, screen_height - self._small_offset))
        self.circle_destroyer_group = pygame.sprite.GroupSingle(CircleDestroyer(
            middle_of_screen + self._small_offset, screen_height - self._small_offset))
        self.circle_generator_group = pygame.sprite.GroupSingle(CircleGenerator(
            middle_of_screen - self._small_offset, screen_height - self._small_offset))
        self.helper_dialogue_group = pygame.sprite.GroupSingle(
            HelperDialogue(middle_of_screen, self._small_offset + 50))
        self.circle_group = pygame.sprite.Group()
        self.arrow_group = pygame.sprite.Group()
        self.ui_elements_group = pygame.sprite.LayeredDirty()
        ui_elements = (self.helper_dialogue_group.sprite, self.button_group.sprite,
                       self.circle_generator_group.sprite, self.circle_destroyer_group)
        self.ui_elements_group.add(*ui_elements)
        self.automaton_var = Automaton(0)
        self.level_automaton = None

        # menu
        self.menu_group = pygame.sprite.GroupSingle(Menu(self.screen))
        self._theme = pygame.mixer.music.load("sounds/main_theme.mp3")

        # sound effects
        self.arrow_delete = pygame.mixer.Sound("sounds/arrow_delete.mp3")
        self.menu_item = pygame.mixer.Sound("sounds/menu_item.mp3")

        # flags
        self.automaton_response = None
        self.button_pressed = False

        # levels
        self.file_handler = FileHandler()
        self.current_section = 0
        self.current_level = 1
        self.level_info = None

        self._action_dict = {
            pygame.K_RETURN: lambda: self._handle_dialogue(),
            pygame.K_ESCAPE: lambda: self._switch_to_menu(),
            pygame.K_SPACE: lambda: self.player_group.sprite.handle_carrying(self.circle_group),
            pygame.K_a: lambda: self._handle_adding_arrow(),
            pygame.K_s: lambda: self.player_group.sprite.handle_variant_change(self.automaton_var, self.circle_group),
            pygame.K_d: lambda: self._handle_deleting_arrow(),
            pygame.K_z: lambda: self._handle_update_transition("z"),
            pygame.K_x: lambda: self._handle_update_transition("x"),
            pygame.K_c: lambda: self._handle_update_transition("c"),
            pygame.K_v: lambda: self._handle_update_transition("v")
        }

    def game_loop(self):
        """Loop in which player input and game events are handled and visualised. Includes menu handling."""
        self.menu_group.sprite.menu_loop()
        self._handle_exiting_menu()

        while self.playing:
            self._event_handler()
            self._update_objects()
            self._draw_objects()

        return self.menu_group.sprite.running_menu

    def _handle_exiting_menu(self):
        """Switches to game on the selected level, and changes the resolution if requested."""
        self._switch_to_game()
        self._handle_loading_level()
        self._change_resolution(self.menu_group.sprite.new_resolution)

    def _switch_to_game(self):
        """Quits game or goes to game based on menu attribute value."""
        if self.menu_group.sprite.quit_game == True:
            self._quit_game()
        else:
            self.current_section = self.menu_group.sprite.current_section
            self.current_level = self.menu_group.sprite.current_level
            self.playing = True

    def _handle_loading_level(self):
        """Saves progress of player, and loads new level. Initialises level and resets values."""
        self._delete_sprites()

        self.circle_generator_group.sprite.reset_count()
        self.circle_group = pygame.sprite.Group()
        self.arrow_group = pygame.sprite.Group()

        self.file_handler.save_unlocked_level(
            self.current_section, self.current_level)
        self.level_info = self.file_handler.load_level(
            self.current_section, self.current_level)
        self.helper_dialogue_group.sprite.initialize_level_dialogue(
            self.level_info)
        self.helper_dialogue_group.sprite.draw_level_text()
        self.environment_group.sprite.input_language = self.level_info.language
        self.automaton_var = Automaton(self.level_info.section)
        self.level_automaton = self.level_info.automaton
        self.automaton_response = None

        self._handle_completion_screen()

    def _delete_sprites(self):
        """Deletes sprites from group before switching to next level."""
        for group in [self.circle_group, self.arrow_group]:
            for sprite in group:
                sprite.kill()

    def _handle_completion_screen(self):
        """Handles going back and from the completion screen. Replayability is possible."""
        if self.level_info.level == 5:
            for sprite in self.ui_elements_group.sprites():
                sprite.visible = False
            self.circle_generator_group.sprite.disable()
            self.environment_group.sprite.change_image("completion")
        else:
            for sprite in self.ui_elements_group.sprites():
                sprite.visible = True
            self.circle_generator_group.sprite.enable()
            self.environment_group.sprite.change_image("environment")

    def _change_resolution(self, new_resolution):
        """Changes the size of the background, moves game elements to relative possition based on new screen size."""
        if new_resolution:
            old_width, old_height = self._screen_width, self._screen_height
            new_width, new_height = new_resolution
            middle_of_screen = new_width / 2

            self.environment_group.sprite.change_resolution(
                (new_width, new_height))
            self.button_group.sprite.position_update(
                middle_of_screen, new_height - self._small_offset, self.button_group.sprite.rect)
            self.circle_generator_group.sprite.position_update(
                middle_of_screen - self._small_offset, new_height - self._small_offset, self.circle_generator_group.sprite.rect)
            self.circle_destroyer_group.sprite.position_update(
                middle_of_screen + self._small_offset, new_height - self._small_offset, self.circle_destroyer_group.sprite.rect)
            self.helper_dialogue_group.sprite.position_update(
                middle_of_screen, self._medium_offset, self.helper_dialogue_group.sprite.rect)

            scale_x = new_width / old_width
            scale_y = new_height / old_height
            self.player_group.sprite.change_resolution(scale_x, scale_y)

            self._screen_width, self._screen_height = new_resolution
            self.menu_group.sprite.new_resolution = None

    def _event_handler(self):
        """Handles player's keypresses and quit event."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._handle_action(event.key)

    def _quit_game(self):
        """Sets up for game quitting by adjusting attribute values."""
        self.menu_group.sprite.running_menu = False
        self.playing = False

    def _handle_action(self, key):
        """Calls lambda function from the action_dict according to event.key."""
        self._action_dict.get(key, lambda: False)()

    def _update_objects(self):
        """Updates position of player, checks collision, handles circle creation and destroying."""
        # player
        # delta_time is used for framerate-independant movement (dt: change in time)
        delta_time = self._clock.tick(self._FPS) / 2
        self._player_movement(delta_time)
        self.player_group.sprite.update_objects(
            self.arrow_group, self.circle_group)

        # button
        self._check_button_collision()

        # circles
        self.circle_generator_group.sprite.handle_new_circles(
            self.player_group, self.circle_group)
        self.circle_destroyer_group.sprite.handle_destroying_circle(
            self.player_group, self.arrow_group, self.automaton_var)

    def _player_movement(self, d_t):
        """Gets pressed keys and hands them over to player movement function."""
        # key is a list of entire keyboard, not one key which is pressed (cannot use to look up keys in dictionary, nor match case)
        key = pygame.key.get_pressed()
        width, height = self.screen.get_size()
        self.player_group.sprite.movement(key, d_t, width, height)

    def _check_button_collision(self):
        """Checks if player is colliding with button,"""
        buttons = pygame.sprite.spritecollide(
            self.player_group.sprite, self.button_group, False, pygame.sprite.collide_mask)

        # if player is colliding with button, and didnt press button yet
        if buttons and not self.button_pressed:
            buttons[0].switch_variant("pressed")
            # game -> button -> automaton (check if it accepts language)
            self.automaton_response = buttons[0].button_pressed(
                self.automaton_var, self.level_automaton)
            self.button_pressed = True
        # player isnt colliding with button, and pressed button before
        elif (not buttons) and self.button_pressed:
            self.button_group.sprite.switch_variant("unpressed")
            self.button_pressed = False

    def _draw_objects(self):
        """Draws all game objects and updates the screen."""
        self.environment_group.draw(self.screen)
        self.environment_group.sprite.draw_input_language(self.screen)
        self.ui_elements_group.draw(self.screen)
        self.arrow_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.player_group.sprite.update_animation()
        self.arrow_group.draw(self.screen)
        self.circle_group.draw(self.screen)
        # in here, so automaton response can overwrite level tips, and showcase its own text
        self.helper_dialogue_group.sprite.draw_automaton_text(
            self.automaton_response)

        # update display
        pygame.display.flip()

    # methods related to to the action_dict (called from handle_action)
    def _handle_dialogue(self):
        """Drawing dialogue text, handing automaton being correct and resetting flag value."""
        # automaton accepts, load next level
        if self.automaton_response == True:
            self._handle_next_level_setup()
            self._handle_loading_level()
        # automaton either doesnt accept, or theres an error
        elif (isinstance(self.automaton_response, tuple) or isinstance(self.automaton_response, int)):
            # reset state, so speech bubble can display tips
            self.automaton_response = None
            # after displaying automatons response, display previous tip
            self.helper_dialogue_group.sprite.level_line_index -= 1
            self.helper_dialogue_group.sprite.draw_level_text()
        # load next useful tip
        else:
            self.helper_dialogue_group.sprite.draw_level_text()

    def _handle_next_level_setup(self):
        """Handling going to next level, or next section if needed."""
        if self.automaton_response == True:
            if self.current_level == self.level_info.max_levels_in_current_section:
                self.current_section += 1
                self.current_level = 1
            else:
                self.current_level += 1

    def _switch_to_menu(self):
        """Setting correct flags to initiate menu being displayed."""
        self.playing = False
        self.menu_group.sprite.running_menu = True
        pygame.mixer.Channel(1).play(self.menu_item)

    def _handle_adding_arrow(self):
        """Handle start and end of arrow creation. Also adding transition to automaton."""
        self.player_group.sprite.handle_arrow_creation(
            self.arrow_group, self.circle_group),
        self.automaton_var.handle_new_transition(
            self.player_group, self.circle_group)

    def _handle_deleting_arrow(self):
        """Deleting arrow and updating automaton adequately."""
        arrows = pygame.sprite.spritecollide(
            self.player_group.sprite, self.arrow_group, False, pygame.sprite.collide_mask) or []

        if arrows:
            self.player_group.sprite.current_arrow = None
            self.arrow_group.remove(arrows[0]) if arrows else None
            self.automaton_var.handle_delete_transition_entirely(
                arrows[0], self.circle_group)
            arrows[0].kill()
            pygame.mixer.Channel(1).play(self.arrow_delete)

    def _handle_update_transition(self, symbol):
        """Adding or removing symbol from arrow and automaton."""
        player_arrows = pygame.sprite.spritecollide(
            self.player_group.sprite, self.arrow_group, False, pygame.sprite.collide_mask)

        if player_arrows:
            self.automaton_response = self.automaton_var.handle_update_transition(
                player_arrows[0], self.circle_group, symbol)

            # if the transition isnt added, remove symbol
            if self.automaton_response != 0:
                player_arrows[0].update_symbol(symbol)
