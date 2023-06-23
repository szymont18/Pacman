from enum import Enum


class MonsterTypes(Enum):
    SKULL = 1
    DEMON = 2
    GHOST = 3

    def __to_string(self):
        if self == MonsterTypes.SKULL:
            return "SKULL"
        if self == MonsterTypes.DEMON:
            return "DEMON"
        if self == MonsterTypes.GHOST:
            return "GHOST"



