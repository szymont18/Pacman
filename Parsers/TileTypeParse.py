from Enums.TileType import *
class TileTypeParser:

    @staticmethod
    def parse(type :int):
        if type == 0:
            return TileType.VOID
        elif type == 1:
            return TileType.WALL
        elif type == 2:
            return TileType.CROSS
        else:
            raise Exception(str(int) + " is not a legal TileType in TileTypeParser/parse")