from enum import Enum

class TileType(Enum):
    WALL = 1
    VOID = 2

    def __to_string(self):
        if self == TileType.WALL:
            return "WALL"
        else:
            return "VOID"

        