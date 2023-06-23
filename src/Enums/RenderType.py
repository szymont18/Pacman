from enum import Enum


class RenderType(Enum):
    SINGLE_IMAGE = 1
    TILE_BY_TILE = 2
    PACMAN_CENTERED = 3 #Pacman jest na srodku mapy i mapa sie porusza

    def __str__(self):
        if self == RenderType.TILE_BY_TILE:
            return "TBT"
        elif self == RenderType.SINGLE_IMAGE:
            return "SI"

