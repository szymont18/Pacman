from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def __to_string(self):
        if self == Direction.UP:
            return "UP"
        elif self == Direction.DN:
            return "DN"
        elif self == Direction.LEFT:
            return "LT"
        else:
            return "RT"