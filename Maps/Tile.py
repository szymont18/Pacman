from Enums import TileType
from Enums.TileType import *

class Tile:
    def __init__(self,TYPE: TileType,mid_x,mid_y):
        self.TYPE = TYPE
        self.POS_X = mid_x #najprawdopodobniej do usuniecia
        self.POS_Y = mid_y
        self.COLLISION = False

        if TYPE == TileType.WALL:
            self.COLLISION = True

