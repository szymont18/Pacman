from Enums import TileType
from Enums.TileType import *
from Enums.Direction import *
from Maps import Tile


class Horizontal_Gate(Tile):
    def __init__(self, TYPE: TileType, mid_x, mid_y):
        super().__init__(TYPE,mid_x,mid_y)
        self.opened = False #Overrides COLLISION variable -> Mobs can walk through the door <==> they are opened

