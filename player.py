import pygame
import math

from arrow import Arrow
from object import Object


class Player(pygame.sprite.Sprite, Object):
    """Represents the playable character. Stores data related to making circles and arrows."""

    def __init__(self, x, y):
        """Creates player at the given coordinates. Initialises needed variables and flags."""
        pygame.sprite.Sprite.__init__(self)
        Object.__init__(self, x, y)
        self._sprite_sheet = pygame.image.load(
            "assets/player_spritesheet.png").convert_alpha()
        # creating a new surface to load only a portion of the sprite sheet
        self.image = pygame.Surface((200, 200), pygame.SRCALPHA)
        self.image.blit(self._sprite_sheet, (0, 0), (800, 0, 200, 200))

        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        # flags
        self._carrying_circle = None
        self._current_arrow = None

        # sound effects
        self.circle_pick_up = pygame.mixer.Sound("sounds/circle_pick_up.mp3")
        self.circle_put_down = pygame.mixer.Sound("sounds/circle_put_down.mp3")
        self.arrow_start = pygame.mixer.Sound("sounds/arrow_start.mp3")
        self.arrow_end = pygame.mixer.Sound("sounds/arrow_end.mp3")

        # animation
        self._last_updated = pygame.time.get_ticks()
        self._frame = 0
        self._animation_list = []
        self._action = 1
        self._animation_init()

        self._action_dict = {
            (-1, 0): "run_left",
            (1, 0): "run_right",
            (0, -1): "run_left",
            (0, 1): "run_right",
            (-0.7, -0.7): "run_left",
            (-0.7, 0.7): "run_left",
            (0.7, -0.7): "run_right",
            (0.7, 0.7): "run_right",
            (0, 0): "stand"
        }

    @property
    def carrying_circle(self):
        return self._carrying_circle

    @carrying_circle.setter
    def carrying_circle(self, value):
        self._carrying_circle = value

    @property
    def current_arrow(self):
        return self._current_arrow

    @current_arrow.setter
    def current_arrow(self, value):
        self._current_arrow = value

    # movement idea from: https://www.youtube.com/watch?v=mWJkvxQXIa8&list=PLRqwX-V7Uu6ZwSmtE13iJBcoI-r4y7iEc&index=2
    def movement(self, key, d_t, width, height):
        """Moves the player inside bounds of the screen based on the key pressed."""
        # bounds of the screen
        x_offset = 100
        y_offset = 150
        left_edge = x_offset
        right_edge = width - x_offset
        top_edge = y_offset
        bottom_edge = height - y_offset

        dx = 0  # change in x
        dy = 0  # change in y

        if key[pygame.K_LEFT] and self.x > left_edge:
            dx += -1
        if key[pygame.K_RIGHT] and self.x < right_edge:
            dx += 1
        if key[pygame.K_UP] and self.y > top_edge:
            dy += -1
        if key[pygame.K_DOWN] and self.y < bottom_edge:
            dy += 1

        # normalising the movement to prevent faster diagonal travel
        if dx != 0 and dy != 0:
            # vector divided by its length -> dx**2 + dy**2 -> 1**2 + 1**2 -> 2
            dx = dx / math.sqrt(2)
            dy = dy / math.sqrt(2)

        # multiplying by d_t to make movement consistent with relation to time
        new_x_position = self.x + dx * d_t
        new_y_position = self.y + dy * d_t
        self.position_update(new_x_position, new_y_position, self.rect)

        # setting what kind of action the player is performing based on the direction of movement
        self._handle_action(dx, dy)

        # if the player somehow escapes the bounds of the screen, teleport him back
        self._check_if_player_in_bounds(
            left_edge, right_edge, top_edge, bottom_edge)

    def _handle_action(self, dx, dy):
        """Depending on direction of movement, sets the current action of the player."""
        action = self._action_dict[(round(dx, 1), round(dy, 1))]

        match action:
            case "stand":
                self._action = 1
                self._frame = 0  # has only one frame, if other action was selected before, frame number could be beyond available frames
            case "run_right":
                self._action = 0
            case "run_left":
                self._action = 2

    def _check_if_player_in_bounds(self, left_edge, right_edge, top_edge, bottom_edge):
        """Checks if the player is inside the bounds of the screen."""
        offset = 50  # if the momentum is large, the player can go slightly beyond the bounds, mitigatting unintended teleportations
        if ((self.x < left_edge - offset) or (self.x > right_edge + offset)):
            self.x = left_edge
        if ((self.y < top_edge - offset) or (self.y > bottom_edge + offset)):
            self.y = top_edge

    def handle_carrying(self, cirlce_group):
        """If player is carrying circle, let it go, if not, pick it up."""
        if self.carrying_circle:
            self.carrying_circle = None
            pygame.mixer.Channel(1).play(self.circle_put_down)
        else:
            circles = pygame.sprite.spritecollide(
                self, cirlce_group, False, pygame.sprite.collide_mask)
            self.carrying_circle = circles[0] if circles else None
            if circles:
                pygame.mixer.Channel(1).play(self.circle_pick_up)

    def handle_variant_change(self, automaton, circle_group):
        """Cycles through variants of circle. Also updates automaton's states."""
        circles = pygame.sprite.spritecollide(
            self, circle_group, False, pygame.sprite.collide_mask)

        circle_variant = circles[0].variant if circles else None
        match circle_variant:
            case "base":  # base -> accepting
                automaton.add_accepting_state(circles[0].number)
                circles[0].switch_variant("accepting")
            case "accepting":  # accepting -> initial
                automaton.remove_accepting_state(circles[0].number)
                automaton.add_initial_state(circles[0].number)
                circles[0].switch_variant("initial")
            case "initial":  # initial -> initial accepting
                automaton.add_accepting_state(circles[0].number)
                circles[0].switch_variant("initial_accepting")
            case "initial_accepting":  # initial accepting -> base
                automaton.remove_initial_state(circles[0].number)
                automaton.remove_accepting_state(circles[0].number)
                circles[0].switch_variant("base")

    def handle_arrow_creation(self, arrow_group, circle_group):
        """Handles creation of arrow."""
        player_circles = pygame.sprite.spritecollide(
            self, circle_group, False, pygame.sprite.collide_mask)

        # arrow is not already being created, and player is colliding with only one circle(making sure its clear which circle is circle from)
        if not self.current_arrow and len(player_circles) == 1:
            self._start_arrow_creation(arrow_group, player_circles)
            pygame.mixer.Channel(1).play(self.arrow_start)

        # arrow is being created, player colliding with only one circle
        elif self.current_arrow and len(player_circles) == 1:
            success = self._end_arrow_creation(arrow_group, circle_group, player_circles)
            if success:
                pygame.mixer.Channel(1).play(self.arrow_end)

    def _start_arrow_creation(self, arrow_group, player_circles):
        """Starts the arrow creation, and adds the arrow to arrow group."""
        # centering arrow on the player position
        self.current_arrow = Arrow(
            player_circles[0].rect.center, player_circles[0].rect.center)
        # adding arrow to arrow_group, so that graphical changes are visible
        arrow_group.add(self.current_arrow)

    def _end_arrow_creation(self, arrow_group, circle_group, player_circles):
        """Checks if arrow doesn't already exist. If not, ends arrow creation."""
        if self._check_arrow_already_exists(arrow_group, circle_group, player_circles):
            return 0

        arrow_circles = pygame.sprite.spritecollide(
            self.current_arrow, circle_group, False, pygame.sprite.collide_mask)
        same_circle = pygame.Rect.collidepoint(
            player_circles[0].rect, self.current_arrow.points[0])

        # loop circle, both ends of arrow collide with the same circle
        if arrow_circles and same_circle:
            self.current_arrow.switch_variant("loop")
        # ending straight circle creation, adding circle_to
        else:
            self.current_arrow.update_point_2(player_circles[0].rect.center)

        self.current_arrow = None
        return 1

    def _check_arrow_already_exists(self, arrow_group, circle_group, player_circles):
        """Checks if arrow from circle_from to the same circle doesn't already exist."""
        # searching for circle_from by finding which circle does the start of arrow intersect with
        circle_from = None
        for circle in circle_group:
            if pygame.Rect.collidepoint(circle.rect, self.current_arrow.points[0]):
                circle_from = circle

        # checking what other arrows intersect circle_from
        potential_duplicates = []
        if circle_from:
            potential_duplicates = pygame.sprite.spritecollide(
                circle_from, arrow_group, False, pygame.sprite.collide_mask)
        if potential_duplicates:
            potential_duplicates.remove(self.current_arrow)

        # finding whether any of potential duplicates start on circle_from
        potential_duplicates_same_start = []
        for p_d in potential_duplicates:
            if pygame.Rect.collidepoint(circle_from.rect, p_d.points[0]):
                potential_duplicates_same_start.append(p_d)

        # checking whether there is any arrow that also ends on the same circle as our potential arrow
        duplicate_found = []
        for p_d in potential_duplicates_same_start:
            if len(p_d.points) == 1:
                point_to = p_d.points[0]
            else:
                point_to = p_d.points[1]
            duplicate_found.append(pygame.Rect.collidepoint(
                player_circles[0].rect, point_to))

        return any(duplicate_found)

    def update_objects(self, arrow_group, circle_group):
        """Updates the position of the carried objects to the current position of the player."""
        # player is only carrying an arrow, updating second point, every arrow begins as straight arrow which has 2 points
        if self.current_arrow:
            self.current_arrow.update_point_2(self.rect.center)

        # player is carrying a circle, and updating arrow associated with the circle too
        if self.carrying_circle:
            # there can be multiple arrows colliding with circle, not just the one player carries
            arrow_circles = pygame.sprite.spritecollide(
                self.carrying_circle, arrow_group, False, pygame.sprite.collide_mask)

            # saving position so that the arrow which collides with circle doesnt get left behind, when circle jumps away suddenly
            # without the copy, python updates the structure, even though the update happens out of the scope of this variable
            previous_circle_position = self.carrying_circle.rect.copy()

            self._update_circle(circle_group)
            self._update_circle_arrows(arrow_circles, previous_circle_position)

    def _update_circle(self, circle_group):
        """Updates circles to the players position."""
        circle_circles = pygame.sprite.spritecollide(
            self.carrying_circle, circle_group, False, pygame.sprite.collide_mask)

        player_circles = pygame.sprite.spritecollide(
            self, circle_group, False, pygame.sprite.collide_mask)

        # update only if circles arent on top of each other (ensures consistency when 2+ circles collide)
        if len(circle_circles) <= 1 or not player_circles:
            self.carrying_circle.position_update(
                self.x, self.y, self.carrying_circle.rect)

    def _update_circle_arrows(self, arrow_circles, previous_circle_position):
        """Updates all of the arrows that are colliding with circle that changed position to their new position."""
        # if circle carried by player collides with arrow, updating the arrow/s too
        # updating arrows (or no arrows) connected to the carried circle
        for arrow in arrow_circles or []:
            arrow.handle_point_update(
                previous_circle_position, self.carrying_circle.rect.center)

    def change_resolution(self, scale_x, scale_y):
        """Change the position of the player relative to the new resolution of screen."""
        new_x = int(self.x * scale_x)
        new_y = int(self.y * scale_y)
        self.position_update(new_x, new_y, self.rect)

    # animation implementation from: https://www.youtube.com/watch?v=nXOVcOBqFwM
    def _animation_init(self):
        """Initialises player's animation."""
        step_counter = 0

        # loading sprites separately
        animation_frames = [6, 1, 6]
        for action in animation_frames:
            frame_list = []
            for _ in range(action):
                frame_list.append(self._get_image(step_counter))
                step_counter += 1
            self._animation_list.append(frame_list)

    def _get_image(self, frame):
        """Gets the current frame of animation from the sprite sheet and returns it as a separate image."""
        width = 200
        height = 200

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self._sprite_sheet, (0, 0),
                   ((frame * width), 0, width, height))

        return image

    def update_animation(self):
        """Cycles through frames of current action after cooldown has been reached."""
        current_time = pygame.time.get_ticks()
        number_of_frames = len(self._animation_list[self._action])
        cooldown = 150
        if current_time - self._last_updated >= cooldown:
            self._frame += 1
            self._frame = self._frame % number_of_frames
            self._last_updated = current_time
        self.image = self._animation_list[self._action][self._frame]
