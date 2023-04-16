from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def __str__(self):
        if self == Direction.UP:
            return "UP"
        elif self == Direction.DOWN:
            return "DOWN"
        elif self == Direction.LEFT:
            return "LEFT"
        else:
            return "RIGHT"