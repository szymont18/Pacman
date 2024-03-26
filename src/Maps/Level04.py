from ..Maps.GameMap import GameMap
from ..Items.BonusLife import BonusLife
from ..Items.BonusMoney import BonusMoney
from ..Items.Slow import Slow
from ..Enums.MonsterTypes import *
from ..Enums.RenderType import *

class Level04(GameMap):
    def __init__(self,field_size):
        super().__init__(MAX_ROW = 17,
                         MAX_COL = 17,
                         FIELD_SIZE = field_size,
                         PACMAN_SPAWN_X=field_size * 8,
                         PACMAN_SPAWN_Y=field_size * 11,
                         POSSIBLE_MONSTERS=[MonsterTypes.SKULL],
                         MONSTER_SPAWN_TILES=[(8, 3)],
                         ONLOAD_SPAWN_MONSTERS=[(MonsterTypes.SKULL, (3, 8)), (MonsterTypes.GHOST, (3, 13))],
                         RED_DOT_POSITIONS=[(1, 1),(15, 1),(6 , 1),(8 , 1),(6 , 15),(1, 15),(8,15),(6,15),(15, 15)],
                         RENDER_TYPE = RenderType.SINGLE_IMAGE)

        self.bonus_probability[BonusLife] = (0.33, None)
        self.bonus_probability[BonusMoney] = (0.33, None)
        self.bonus_probability[Slow] = (0.33, None)

        self.load_map(self.get_tiles_path())
        self.load_items()


    def get_image_path(self):
        return "resources/maps/Level4.png"

    def get_tiles_path(self): #sciezka gdzie jest plik tekstowy opisujacy wyglad mapy
        return "resources/maps/level4.txt"

    def get_music_path(self):
        return "resources/music/04.MID"
