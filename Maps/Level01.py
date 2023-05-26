from Maps.GameMap import GameMap
from Items.BonusLife import BonusLife
from Items.BonusMoney import BonusMoney
from Enums.MonsterTypes import *


class Level01(GameMap):
    def __init__(self, max_row, max_col, field_size):
        super().__init__(max_row, max_col, field_size,
                         PACMAN_SPAWN_X = field_size * 2,
                         PACMAN_SPAWN_Y = field_size * 10,
                         POSSIBLE_MONSTERS = [MonsterTypes.SKULL],
                         MONSTER_SPAWN_TILES = [(8, 8)],
                         ONLOAD_SPAWN_MONSTERS = [(MonsterTypes.SKULL, (8, 8))],
                         RED_DOT_POSITIONS = [(1, 1),(10, 1),(15, 1),(1, 15), (10, 15),(15, 15)])

        self.load_map(self.get_tiles_path())
        self.load_items()

        self.bonus_probability[BonusLife] = (0.5, None)
        self.bonus_probability[BonusMoney] = (0.5, None)

        self.redDotPositions = [(1, 1),
                           (10, 1),
                           (15, 1),
                           (1, 15),
                           (10, 15),
                           (15, 15)]

    def get_image_path(self):
        return "resources/maps/Level01.png"

    def get_tiles_path(self):
        return "resources/maps/Level01.txt"

    def get_music_path(self):
        return "resources/music/01.MID"


