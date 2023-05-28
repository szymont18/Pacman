from enum import Enum


class TileType(Enum):
    VOID = 0
    WALL = 1
    CROSS = 2
    HORIZONTAL_GATE = 3
    VERTICAL_GATE = 4
    LAVA = 5


    def __str__(self):
        if self == TileType.WALL:
            return "WALL"
        elif self == TileType.VOID:
            return "VOID"
        elif self == TileType.CROSS:
            return "CROSS"
        elif self == TileType.HORIZONTAL_GATE:
            return "HGATE"
        elif self == TileType.VERTICAL_GATE:
            return "VGATE"
        elif self == TileType.LAVA:
            return "LAVA"

