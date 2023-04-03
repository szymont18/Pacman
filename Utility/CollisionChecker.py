from MapElements import MapElement
from Enums import Direction as Direction
from Enums.Direction import *
from Utility.PairRowCol import PairRowCol


class CollisionChecker:
    def __init__(self, ENGINE,MAP):
        self.__ENGINE = ENGINE
        self.__MAP = MAP

    # Zwraca informacje czy dany element moze sie poruszyc w kierunku direction
    def can_move(self, element: MapElement, direction: Direction):
        if direction == None:
            return False

        speed_shift = max(element.get_speed(), 3)

        # Wspolrzedne wierzcholkow prostokata wyznaczajacego SOLID_AREA elementu
        element_left_x = element.get_pos_x() + element.SOLID_AREA.x
        element_right_x = element.get_pos_x() + element.SOLID_AREA.x + element.SOLID_AREA.width
        element_top_y = element.get_pos_y() + element.SOLID_AREA.y
        element_bottom_y = element.get_pos_y() + element.SOLID_AREA.y + element.SOLID_AREA.height

        # Translacja powyzszych wartosci na kolumny (Pacmana)
        element_left_col = element_left_x // self.__ENGINE.FIELD_SIZE
        element_right_col = element_right_x // self.__ENGINE.FIELD_SIZE

        element_top_row = element_top_y // self.__ENGINE.FIELD_SIZE
        element_bottom_row = element_bottom_y // self.__ENGINE.FIELD_SIZE

        if direction == Direction.UP:
            if element.get_direction() == Direction.LEFT or element.get_direction() == Direction.RIGHT:
                element_top_row = (element_top_y - 3 * speed_shift) // self.__ENGINE.FIELD_SIZE
            else: element_top_row = (element_top_y - speed_shift) // self.__ENGINE.FIELD_SIZE

            element_top_row = element_top_row % self.__MAP.MAX_ROW
            #Czy mozna wykonac ruch
            if (self.__MAP.get_collision_status(element_top_row, element_left_col) or
                self.__MAP.get_collision_status(element_top_row, element_right_col)):
                return False

        elif direction == Direction.DOWN:
            if element.get_direction() == Direction.LEFT or element.get_direction() == Direction.RIGHT:
                element_bottom_row = (element_bottom_y + 3 * speed_shift) // self.__ENGINE.FIELD_SIZE
            else:
                element_bottom_row = (element_bottom_y + speed_shift) // self.__ENGINE.FIELD_SIZE

            element_bottom_row = element_bottom_row % self.__MAP.MAX_ROW

            # Czy mozna wykonac ruch
            if (self.__MAP.get_collision_status(element_bottom_row, element_left_col) or
                    self.__MAP.get_collision_status(element_bottom_row, element_right_col)):
                return False

        elif direction == Direction.LEFT:
            if element.get_direction() == Direction.UP or element.get_direction() == Direction.DOWN:
                element_left_col = (element_left_x - 3 * speed_shift) // self.__ENGINE.FIELD_SIZE
            else:
                element_left_col = (element_left_x - speed_shift) // self.__ENGINE.FIELD_SIZE

            element_left_col = element_left_col % self.__MAP.MAX_COL

            # Czy mozna wykonac ruch
            if (self.__MAP.get_collision_status(element_top_row, element_left_col) or
                    self.__MAP.get_collision_status(element_bottom_row, element_left_col)):
                return False

        elif direction == Direction.RIGHT:
            if element.get_direction() == Direction.UP or element.get_direction() == Direction.DOWN:
                element_right_col = (element_right_x + 3 * speed_shift) // self.__ENGINE.FIELD_SIZE
            else:
                element_right_col = (element_right_x + speed_shift) // self.__ENGINE.FIELD_SIZE

            element_right_col = element_right_col % self.__MAP.MAX_COL

            # Czy mozna wykonac ruch
            if (self.__MAP.get_collision_status(element_top_row, element_right_col) or
                    self.__MAP.get_collision_status(element_bottom_row, element_right_col)):
                return False
        return True

    def check_for_items(self, element):
        # Wspolrzedne wierzcholkow prostokata wyznaczajacego SOLID_AREA elementu
        element_left_x = element.get_pos_x() + element.SOLID_AREA.x
        element_right_x = element.get_pos_x() + element.SOLID_AREA.x + element.SOLID_AREA.width
        element_top_y = element.get_pos_y() + element.SOLID_AREA.y
        element_bottom_y = element.get_pos_y() + element.SOLID_AREA.y + element.SOLID_AREA.height

        # Translacja powyzszych wartosci na kolumny
        element_left_col = element_left_x // self.__ENGINE.FIELD_SIZE
        element_right_col = element_right_x // self.__ENGINE.FIELD_SIZE

        element_top_row = element_top_y // self.__ENGINE.FIELD_SIZE
        element_bottom_row = element_bottom_y // self.__ENGINE.FIELD_SIZE

        direction = element.get_direction()

        if direction == Direction.UP:
            para1 = PairRowCol(element_top_row,element_left_col)
            para2 = PairRowCol(element_top_row,element_right_col)

            item1 = self.__MAP.get_items().get(para1)
            item2 = self.__MAP.get_items().get(para2)

            if item1 != None and element.SOLID_AREA.contains(item1.SOLID_AREA):
                return item1
            if item2 != None and element.SOLID_AREA.contains(item2.SOLID_AREA):
                return item2

        elif direction == Direction.DOWN:
            para1 = PairRowCol(element_bottom_row,element_left_col)
            para2 = PairRowCol(element_bottom_row,element_right_col)

            item1 = self.__MAP.get_items().get(para1)
            item2 = self.__MAP.get_items().get(para2)


            if item1 != None and element.SOLID_AREA.contains(item1.SOLID_AREA):
                return item1
            if item2 != None and element.SOLID_AREA.contains(item2.SOLID_AREA):
                return item2

        elif direction == Direction.LEFT:
            para1 = PairRowCol(element_top_row,element_left_col)
            para2 = PairRowCol(element_bottom_row,element_left_col)

            item1 = self.__MAP.get_items().get(para1)
            item2 = self.__MAP.get_items().get(para2)


            if item1 != None and element.SOLID_AREA.contains(item1.SOLID_AREA):
                return item1
            if item2 != None and element.SOLID_AREA.contains(item2.SOLID_AREA):
                return item2

        elif direction == Direction.RIGHT:
            para1 = PairRowCol(element_top_row,element_right_col)
            para2 = PairRowCol(element_bottom_row,element_right_col)

            item1 = self.__MAP.get_items().get(para1)
            item2 = self.__MAP.get_items().get(para2)


            if item1 != None and element.SOLID_AREA.contains(item1.SOLID_AREA):
                return item1
            if item2 != None and element.SOLID_AREA.contains(item2.SOLID_AREA):
                return item2

        return None


