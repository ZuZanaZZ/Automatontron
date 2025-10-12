import pygame
import math

from abc import ABC, abstractmethod
from draw_text import DrawText
from config.global_vars import color_normal, color_dark, font


class ArrowVariant(ABC, DrawText):
    """Describes what attributes and methods should an arrow variant have."""

    def __init__(self):
        """Initialises a blank arrow."""
        self._variant = None
        self._symbols = []
        # both implementations use different number of points, initialising as none
        self._points = None
        self._image = None
        self._rect = None
        self._mask = None

    @abstractmethod
    def _materialisation(self):
        pass

    @abstractmethod
    def add_symbol(self, symbol):
        pass

    @abstractmethod
    def remove_symbol(self, symbol):
        pass


class StraightVariant(ArrowVariant):
    """Straight variant of the arrow. Represents transition from one circle to the next."""

    def __init__(self, points):
        """Create and materialise a blank straight arrow."""
        super().__init__()
        self._variant = "straight"
        self._points = points
        self._materialisation()

    def _materialisation(self):
        """Calculates offset points for the arrow and draws it with symbols."""
        padding = 70
        x1, y1 = self._points[0]
        x2, y2 = self._points[1]
        width = abs(x2 - x1) + padding
        height = abs(y2 - y1) + padding

        # making new surface for drawing arrow on. adding aditional padding, so arrow wont get cut off
        self._image = pygame.Surface(
            (width + padding, height + padding), pygame.SRCALPHA).convert_alpha()

        # finding coordinates of top left corner to start drawing process corectly
        origin_x = min(x1, x2)
        origin_y = min(y1, y2)

        # converting screen coordinates to relative coordintes of arrow image: https://stackoverflow.com/questions/23648450/python-surface-real-position-coordinates-of-pygame-mouse-get-pos-and-rect-collid
        # adding padding so that arrow isnt shifted (the padding added from height and width changes the actual starting point of the arrow)
        rel_x1 = x1 - origin_x + padding
        rel_y1 = y1 - origin_y + padding
        rel_x2 = x2 - origin_x + padding
        rel_y2 = y2 - origin_y + padding

        # drawing the arrow
        symbols, tip = self._calculate_offset_points((rel_x1, rel_y1), (rel_x2, rel_y2))
        symbols_x, symbols_y = symbols
        tip_x, tip_y = tip

        self._draw_rotated_arc(symbols, tip)
        self._draw_arrowhead(symbols, tip)

        # drawing symbols
        # list to string: https://stackoverflow.com/questions/12453580/how-to-concatenate-join-items-in-a-list-to-a-single-string
        symbols = ", ".join(self._symbols)
        center_x = ((symbols_x + tip_x) / 2) # center of line, (a + b) / 2
        center_y = ((symbols_y + tip_y) / 2)
        self.draw_text(self._image, symbols, font,
                       color_dark, center_x, center_y)

        # removing padding makes the arrow appear to start at the circle (if padding left in, the surface would start from the circle, making the arrow look shifted)
        self._rect = self._image.get_rect(
            topleft=(origin_x - padding, origin_y - padding))
        self._mask = pygame.mask.from_surface(self._image)

    def _calculate_offset_points(self, base_point, tip_point):
        """Calculates new points offset from the base and tip points at given angle and radius."""
        offset_angle_rad = math.radians(45) # offset the point from direct line between the circles

        # calculate angle from direction vector
        dx, dy = self._calculate_direction_vector(base_point, tip_point)
        angle_rad = math.atan2(dy, dx)

        # offset base point by rotating by offset_angle_rad from the original angle
        offset_angle = angle_rad - offset_angle_rad 
        new_base_point = self._calculate_offset_point(base_point, offset_angle)
        
        # offset tip point by offset_angle_rad and rotate to other side, so its facing correctly
        offset_angle = angle_rad + math.radians(180) + offset_angle_rad 
        new_tip_point = self._calculate_offset_point(tip_point, offset_angle)
        
        return new_base_point, new_tip_point
    
    def _draw_rotated_arc(self, base_point, tip_point):
        """Draws arc of the arrow and correctly rotates it."""
        curvature = 60
        line_width = 5

        # getting middle of distance between the two points
        center_x = (base_point[0] + tip_point[0]) / 2
        center_y = (base_point[1] + tip_point[1]) / 2

        dx, dy = self._calculate_direction_vector(base_point, tip_point)
        angle_deg = self._calculate_vector_angle(dx, dy)
        length = self._calculate_vector_length(dx, dy)

        # creating surface for the arc, and drawing it on
        arc_surface = pygame.Surface((length, curvature), pygame.SRCALPHA)
        pygame.draw.arc(arc_surface, color_normal, arc_surface.get_rect(), 0, math.pi, line_width)

        # rotating surface and its position around the center between the two points
        rotated_surf = pygame.transform.rotate(arc_surface, angle_deg)
        rotated_rect = rotated_surf.get_rect(center=(center_x, center_y))

        self._image.blit(rotated_surf, rotated_rect)

    def _draw_arrowhead(self, base_point, tip_point):
        """Draws polygon in the shape of an arrowhead and correctly rotates it."""
        # https://stackoverflow.com/questions/10473930/how-do-i-find-the-angle-between-2-points-in-pygame
        # getting change in x and y between the start and end of the arrow
        dx, dy = self._calculate_direction_vector(base_point, tip_point)
        angle_deg = self._calculate_vector_angle(dx, dy)
        angle_deg -= 30 # rotating angle slightly, so it looks like the arrowhead follows the arc line

        # defining arrowhead, pointing to the right -> at 0 degrees arrowhead points to right
        tip_offset = 40
        side_offset = 20
        arrowhead = [(tip_offset, side_offset), (0, 0), (0, side_offset * 2)]

        # making arrowhead be its own surface, so it can be rotated independantly from the line of the arrow
        arrowhead_surface = pygame.Surface(
            (tip_offset,  side_offset * 2), pygame.SRCALPHA).convert_alpha()

        # drawing the arrowhead on the surface and rotating
        pygame.draw.polygon(arrowhead_surface, color_normal, arrowhead)
        arrowhead_surface_rotated = pygame.transform.rotate(
            arrowhead_surface, angle_deg)

        # drawing the arrowhead on the main surface at the correct position
        rect_position = arrowhead_surface_rotated.get_rect(center=tip_point)
        self._image.blit(arrowhead_surface_rotated, rect_position)

    def _calculate_direction_vector(self, point_1, point_2):
        """Calculates vector of direction between two points."""
        x1, y1 = point_1
        x2, y2 = point_2
        dx = x2 - x1  # x difference between point_1 and point_2
        dy = y2 - y1  # y difference between point_1 and point_2

        return dx, dy
    
    def _calculate_vector_angle(self, dx, dy):
        """Calculates the angle of the given vector in degrees."""
        # - dy to flip the axis, in cartesian coordinates y increases up, in pygame y increases down
        angle_rad = math.atan2(- dy, dx) 
        # converting to degrees to be used with rotate funcion
        angle_deg = math.degrees(angle_rad)

        return angle_deg
    
    def _calculate_vector_length(self, dx, dy):
        """Calculates the length of the vector."""
        # calculating hypotenuse -> a^2 + b^2 = c^2 -> a = dy, b = dy
        length = math.sqrt(dx**2 + dy**2)
        # if length is 0, assign 1. preventing division by 0
        length = length if length >= 1 else 1

        return length
    
    def _calculate_offset_point (self, point, offset_angle):
        """Calculates a new point offset from the original by the given angle"""
        circle_radius = 30 # distance to offset from middle of circle
        new_point_x = point[0] + circle_radius * math.cos(offset_angle) # rotates on x axis by given angle
        new_point_y = point[1] + circle_radius * math.sin(offset_angle) # rotates on y axis by given angle
        
        return (new_point_x, new_point_y)

    def add_symbol(self, symbol):
        """Adds symbol to the arrow and visualises the change."""
        self._symbols.append(symbol)
        self._materialisation()

    def remove_symbol(self, symbol):
        """Removes symbol from the arrow and visualises the change."""
        self._symbols.remove(symbol)
        self._materialisation()

    def update_point_1(self, point):
        self._points[0] = point

    def update_point_2(self, point):
        self._points[1] = point

class LoopVariant(ArrowVariant):
    """Loop variant of the arrow. Represents transition from one state to the same one."""

    def __init__(self, points):
        """Create and materialise a blank Loop arrow."""
        super().__init__()
        self._variant = "loop"
        self._image = pygame.image.load(
            "assets/loop_arrow.png").convert_alpha()

        new_point = points[0]
        # adjusting y height, so that arrow is on top of the circle
        new_point = (new_point[0], new_point[1] - 25)
        self._rect = self._image.get_rect(midbottom=new_point)
        self._points = [new_point]
        self._materialisation()

    def _materialisation(self):
        """Loads a picture of the loop arrow and draws it with symbols."""
        # make bigger surface, so multiple symbols wont get cut off when blitting
        bigger_surface = pygame.Surface((120, 50), pygame.SRCALPHA)
        # load new_image of arrow, so that the old symbols dont persist
        loop_arrow = pygame.image.load("assets/loop_arrow.png").convert_alpha()
        bigger_surface.blit(loop_arrow, (35, 0))
        self._image = bigger_surface

        symbols = ", ".join(self._symbols)
        self.draw_text_centered(self._image, symbols, font, color_dark)

        # updating the position of the rectangle
        self._rect = self._image.get_rect(midbottom=self._points[0])
        self._mask = pygame.mask.from_surface(self._image)

    def add_symbol(self, symbol):
        """Adds symbol to the arrow and visualises the change."""
        self._symbols.append(symbol)
        self._materialisation()

    def remove_symbol(self, symbol):
        """Removes symbol from the arrow and visualises the change."""
        self._symbols.remove(symbol)
        self._materialisation()

    def update_point(self, point):
        """Updates and adjusts the height of arrow point so it isn't obscured by the circle."""
        y_height = 25
        new_point = (point[0], point[1] - y_height)
        self._points = [new_point]
