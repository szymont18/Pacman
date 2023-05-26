from Maps.GameMap import GameMap
from Maps.Tile import *
from Items.Slow import Slow
from Enums.MonsterTypes import *
from Items.BonusLife import BonusLife
from Items.Nuke import Nuke
from Items.BonusMoney import BonusMoney


class Level07(GameMap):
    def __init__(self,max_row,max_col,field_size):
        super().__init__(max_row, max_col, field_size,
                         PACMAN_SPAWN_X=field_size * 8,
                         PACMAN_SPAWN_Y=field_size * 12,
                         POSSIBLE_MONSTERS=[MonsterTypes.SKULL],
                         MONSTER_SPAWN_TILES=[(8, 3)],
                         ONLOAD_SPAWN_MONSTERS=[(MonsterTypes.SKULL,(3,8))],
                         RED_DOT_POSITIONS=[(1, 1),(1, 15),(3,3),(3,13),(7,8),(12,3),(12,13),(15,15),(15,1)]
                         )

        self.bonus_probability[Slow] = (0.3, None)
        self.bonus_probability[BonusLife] = (0.3, None)
        self.bonus_probability[Nuke] = (0.3, None)
        self.bonus_probability[BonusMoney] = (0.1, None)

        self.load_map(self.get_tiles_path())
        self.load_items()


    def get_image_path(self):
        return "resources/maps/Level07.png"

    def get_tiles_path(self): #sciezka gdzie jest plik tekstowy opisujacy wyglad mapy
        return "resources/maps/Level07.txt"

    def get_music_path(self):
        return "resources/music/13.MID"
