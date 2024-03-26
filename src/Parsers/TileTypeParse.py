from ..Enums.TileType import *
class TileTypeParser:

    @staticmethod
    def parse(type :int):
        if type == 0:
            return TileType.VOID
        elif type == 1:
            return TileType.WALL
        elif type == 2:
            return TileType.CROSS
        elif type == 3:
            return TileType.HORIZONTAL_GATE
        elif type == 4:
            return TileType.VERTICAL_GATE
        elif type == 5:
            return TileType.LAVA

        else:
            raise Exception(str(int) + " is not a legal TileType in TileTypeParser/parse")