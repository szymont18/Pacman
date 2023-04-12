from Enums import TileType
from Enums.TileType import *
from Enums.Direction import *

class Tile:
    def __init__(self,TYPE: TileType,mid_x,mid_y):
        self.TYPE = TYPE
        self.POS_X = mid_x #najprawdopodobniej do usuniecia
        self.POS_Y = mid_y
        self.COLLISION = False
        self.__possible_turns = [] #skrety jakie mozna wykonac stojac na tym polu (potwory losuja nastepny ruch po uderzeniu w sciane dzieki temu)

        if TYPE == TileType.WALL:
            self.COLLISION = True

    def add_possible_turn(self,turn : Direction):
        self.__possible_turns.append(turn)

    def get_possible_turns(self):
        return self.__possible_turns


