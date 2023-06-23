import pygame

from MapElements import MapElement
from Enums import Direction as Direction
from Enums.Direction import *
from Items import Item


class CollisionChecker:
    def __init__(self, ENGINE, MAP):
        self.__ENGINE = ENGINE
        self.__MAP = MAP

    # Returns whether an element can move in a direction
    def can_move(self, element: MapElement, direction: Direction):
        if direction is None:
            return False

        speed_shift = max(element.get_speed(), 3)

        # The coordinates of the vertices of the rectangle defining the SOLID_AREA of the element
        element_left_x = element.get_pos_x() + element.SOLID_AREA.x
        element_right_x = element.get_pos_x() + element.SOLID_AREA.x + element.SOLID_AREA.width
        element_top_y = element.get_pos_y() + element.SOLID_AREA.y
        element_bottom_y = element.get_pos_y() + element.SOLID_AREA.y + element.SOLID_AREA.height

        # Translating the above values into columns (Pacman)
        element_left_col = element_left_x // self.__ENGINE.FIELD_SIZE
        element_right_col = element_right_x // self.__ENGINE.FIELD_SIZE

        element_top_row = element_top_y // self.__ENGINE.FIELD_SIZE
        element_bottom_row = element_bottom_y // self.__ENGINE.FIELD_SIZE

        if direction == Direction.UP:
            if element.get_direction() == Direction.LEFT or element.get_direction() == Direction.RIGHT:
                element_top_row = (element_top_y - 3 * speed_shift) // self.__ENGINE.FIELD_SIZE
            else:
                element_top_row = (element_top_y - speed_shift) // self.__ENGINE.FIELD_SIZE

            element_top_row = element_top_row % self.__MAP.MAX_ROW
            # Can element move ?
            if (self.__MAP.get_collision_status(element_top_row, element_left_col) or
                    self.__MAP.get_collision_status(element_top_row, element_right_col)):
                return False

        elif direction == Direction.DOWN:
            if element.get_direction() == Direction.LEFT or element.get_direction() == Direction.RIGHT:
                element_bottom_row = (element_bottom_y + 3 * speed_shift) // self.__ENGINE.FIELD_SIZE
            else:
                element_bottom_row = (element_bottom_y + speed_shift) // self.__ENGINE.FIELD_SIZE

            element_bottom_row = element_bottom_row % self.__MAP.MAX_ROW

            # Can element move ?
            if (self.__MAP.get_collision_status(element_bottom_row, element_left_col) or
                    self.__MAP.get_collision_status(element_bottom_row, element_right_col)):
                return False

        elif direction == Direction.LEFT:
            if element.get_direction() == Direction.UP or element.get_direction() == Direction.DOWN:
                element_left_col = (element_left_x - 3 * speed_shift) // self.__ENGINE.FIELD_SIZE
            else:
                element_left_col = (element_left_x - speed_shift) // self.__ENGINE.FIELD_SIZE

            element_left_col = element_left_col % self.__MAP.MAX_COL

            # Can element move ?
            if (self.__MAP.get_collision_status(element_top_row, element_left_col) or
                    self.__MAP.get_collision_status(element_bottom_row, element_left_col)):
                return False

        elif direction == Direction.RIGHT:
            if element.get_direction() == Direction.UP or element.get_direction() == Direction.DOWN:
                element_right_col = (element_right_x + 3 * speed_shift) // self.__ENGINE.FIELD_SIZE
            else:
                element_right_col = (element_right_x + speed_shift) // self.__ENGINE.FIELD_SIZE

            element_right_col = element_right_col % self.__MAP.MAX_COL

            # Can element move ?
            if (self.__MAP.get_collision_status(element_top_row, element_right_col) or
                    self.__MAP.get_collision_status(element_bottom_row, element_right_col)):
                return False
        return True

    def check_for_items(self, element):
        # The coordinates of the vertices of the rectangle defining the SOLID_AREA of the element
        element_left_x = element.get_pos_x() + element.SOLID_AREA.x
        element_right_x = element.get_pos_x() + element.SOLID_AREA.x + element.SOLID_AREA.width
        element_top_y = element.get_pos_y() + element.SOLID_AREA.y
        element_bottom_y = element.get_pos_y() + element.SOLID_AREA.y + element.SOLID_AREA.height

        # Translate the above values into columns
        element_left_col = element_left_x // self.__ENGINE.FIELD_SIZE
        element_right_col = element_right_x // self.__ENGINE.FIELD_SIZE

        element_top_row = element_top_y // self.__ENGINE.FIELD_SIZE
        element_bottom_row = element_bottom_y // self.__ENGINE.FIELD_SIZE

        direction = element.get_direction()

        if direction == Direction.UP:
            para1 = (element_top_row, element_left_col)
            para2 = (element_top_row, element_right_col)

            item1 = self.__MAP.get_items().get(para1)
            item2 = self.__MAP.get_items().get(para2)

            if item1 is not None and element.SOLID_AREA.contains(item1.SOLID_AREA):
                return item1
            if item2 is not None and element.SOLID_AREA.contains(item2.SOLID_AREA):
                return item2

        elif direction == Direction.DOWN:
            para1 = (element_bottom_row, element_left_col)
            para2 = (element_bottom_row, element_right_col)

            item1 = self.__MAP.get_items().get(para1)
            item2 = self.__MAP.get_items().get(para2)

            if item1 is not None and element.SOLID_AREA.contains(item1.SOLID_AREA):
                return item1
            if item2 is not None and element.SOLID_AREA.contains(item2.SOLID_AREA):
                return item2

        elif direction == Direction.LEFT:
            para1 = (element_top_row, element_left_col)
            para2 = (element_bottom_row, element_left_col)

            item1 = self.__MAP.get_items().get(para1)
            item2 = self.__MAP.get_items().get(para2)

            if item1 is not None and element.SOLID_AREA.contains(item1.SOLID_AREA):
                return item1
            if item2 is not None and element.SOLID_AREA.contains(item2.SOLID_AREA):
                return item2

        elif direction == Direction.RIGHT:
            para1 = (element_top_row, element_right_col)
            para2 = (element_bottom_row, element_right_col)

            item1 = self.__MAP.get_items().get(para1)
            item2 = self.__MAP.get_items().get(para2)

            if item1 is not None and element.SOLID_AREA.contains(item1.SOLID_AREA):
                return item1
            if item2 is not None and element.SOLID_AREA.contains(item2.SOLID_AREA):
                return item2

        return None

    # Method verifies if element/item colides with pacman
    def crosses_with_pacman(self, element):
        pacman_pos_x, pacman_pos_y = self.__ENGINE.get_pacman_pos()
        solid_area = element.get_solid_area()

        rect1 = pygame.Rect(element.get_pos_x() + solid_area.left,
                            element.get_pos_y() + solid_area.top,
                            solid_area.width,
                            solid_area.height)

        rect2 = pygame.Rect(pacman_pos_x, pacman_pos_y, self.__ENGINE.FIELD_SIZE - 10,
                            self.__ENGINE.FIELD_SIZE - 10)

        return rect1.colliderect(rect2)

