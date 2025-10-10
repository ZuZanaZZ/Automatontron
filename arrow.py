import pygame

from arrow_variant import StraightVariant, LoopVariant

class Arrow(pygame.sprite.Sprite):
    """Arrow with symbols."""

    def __init__(self, point_1, point_2):
        """Creates, materialises and houses the variant of the arrow."""
        pygame.sprite.Sprite.__init__(self)
        # point_1 = (x,y) the arrow is defined by a list of points, not by x, y coordinates, so it doesn't inherit from Object
        self.variant_var = StraightVariant([point_1, point_2])
        self._materialisation()

        # sound effects
        self.symbol_add = pygame.mixer.Sound("sounds/symbol_add.mp3")
        self.symbol_remove = pygame.mixer.Sound("sounds/symbol_remove.mp3")

    @property
    def variant(self):
        return self.variant_var._variant

    @property
    def symbols(self):
        return self.variant_var._symbols

    @property
    def points(self):
        return self.variant_var._points

    @property
    def image(self):
        return self.variant_var._image

    @property
    def rect(self):
        return self.variant_var._rect

    @property
    def mask(self):
        return self.variant_var._mask

    def switch_variant(self, new_variant):
        """Switches variant of the arrow according to the selected new variant."""
        points = self.points

        match new_variant:
            case "straight":
                self.variant_var = StraightVariant(points)
            case "loop":
                self.variant_var = LoopVariant(points)

        self._materialisation()

    def _materialisation(self):
        """Materialises the full arrow, from its parts."""
        self.variant_var._materialisation()

    def update_symbol(self, symbol):
        """Handles adding or removing symbol. If there is already symbol its removed. If not, its added."""
        if symbol in self.variant_var._symbols:
            self.variant_var.remove_symbol(symbol)
            pygame.mixer.Channel(1).play(self.symbol_remove)
        else:
            self.variant_var.add_symbol(symbol)
            pygame.mixer.Channel(1).play(self.symbol_add)

        # updates arrow, so the changes are visible
        self._materialisation()

    def handle_point_update(self, previous_position, new_position):
        """Selects correct point of arrow and updates it from previous position to new one."""
        if self.variant == "loop":
            self.update_point(new_position)
        # straight arrow, choosing which end to update
        elif pygame.Rect.collidepoint(previous_position, self.points[0]):
            self.update_point_1(new_position)
        elif pygame.Rect.collidepoint(previous_position, self.points[1]):
            self.update_point_2(new_position)

    def update_point_1(self, point):
        """Updating point 1 of straight arrow variant to new position."""
        self.variant_var.update_point_1(point)
        self._materialisation()

    def update_point_2(self, point):
        """Updating point 2 of straight arrow variant to new position."""
        self.variant_var.update_point_2(point)
        self._materialisation()

    def update_point(self, point):
        """Updating point of loop arrow variant to new position."""
        self.variant_var.update_point(point)
        self._materialisation()
