from Maps.GameMap import GameMap
from Items.BonusLife import BonusLife
from Items.BonusMoney import BonusMoney
from Items.Slow import Slow
from Items.Nuke import Nuke
from Enums.MonsterTypes import *


class Level05(GameMap):
    def __init__(self,max_row,max_col,field_size):
        super().__init__(max_row, max_col, field_size,
                         PACMAN_SPAWN_X=field_size * 1,
                         PACMAN_SPAWN_Y=field_size * 15,
                         POSSIBLE_MONSTERS=[MonsterTypes.SKULL],
                         MONSTER_SPAWN_TILES=[(15, 1)],
                         ONLOAD_SPAWN_MONSTERS=[(MonsterTypes.SKULL,(1,15)),(MonsterTypes.DEMON,(1,1)),(MonsterTypes.GHOST,(1,8))],
                         RED_DOT_POSITIONS=[(1,1),(3, 1),(8,1),
                                            (1,15),(3, 15),(8,15),
                                            (10,1),(10,15)]
                         )

        self.bonus_probability[BonusLife] = (0.4, None)
        self.bonus_probability[BonusMoney] = (0.2, None)
        self.bonus_probability[Slow] = (0.4, None)

        self.load_map(self.get_tiles_path())
        self.load_items()


    def get_image_path(self):
        return "resources/maps/Level05.png"

    def get_tiles_path(self): #sciezka gdzie jest plik tekstowy opisujacy wyglad mapy
        return "resources/maps/Level05.txt"

    def get_music_path(self):
        return "resources/music/05.MID"
