from Enums import TileType
from Enums.TileType import *
from Enums.Direction import *


class Tile:
    def __init__(self, TYPE: TileType, mid_x=0, mid_y=0):
        self.TYPE = TYPE
        self.POS_X = mid_x  # Probably to remove
        self.POS_Y = mid_y
        self.COLLISION = True
        self.__possible_turns = []  # turns that can be made while standing on this field
        # (monsters draw the next move after hitting the wall thanks to this)

        if TYPE == TileType.VOID:
            self.COLLISION = False

    #Which way can mobs go while standing on this tile
    def add_possible_turn(self, turn: Direction):
        self.__possible_turns.append(turn)

    def get_possible_turns(self):
        return self.__possible_turns
