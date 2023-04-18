from Enums import TileType
from Enums.TileType import *
from Enums.Direction import *


class Tile:
    def __init__(self, TYPE: TileType, mid_x, mid_y):
        self.TYPE = TYPE
        self.POS_X = mid_x  # Probably to remove
        self.POS_Y = mid_y
        self.COLLISION = False
        self.__possible_turns = []  # turns that can be made while standing on this field
        # (monsters draw the next move after hitting the wall thanks to this)

        if TYPE == TileType.WALL:
            self.COLLISION = True

    def add_possible_turn(self, turn: Direction):
        self.__possible_turns.append(turn)

    def get_possible_turns(self):
        return self.__possible_turns
