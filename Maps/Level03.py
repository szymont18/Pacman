from Maps.GameMap import GameMap
from Items.BonusLife import BonusLife
from Items.BonusMoney import BonusMoney
from Enums.MonsterTypes import *
from Enums.RenderType import *

class Level03(GameMap):
    def __init__(self,field_size):
        super().__init__(MAX_ROW = 17,
                         MAX_COL = 17,
                         FIELD_SIZE = field_size,
                         PACMAN_SPAWN_X=field_size * 8,
                         PACMAN_SPAWN_Y=field_size * 15,
                         POSSIBLE_MONSTERS=[MonsterTypes.SKULL],
                         MONSTER_SPAWN_TILES=[(8, 7)],
                         ONLOAD_SPAWN_MONSTERS=[(MonsterTypes.SKULL, (8, 8)), (MonsterTypes.DEMON, (1, 8))],
                         RED_DOT_POSITIONS=[(1, 1),(15, 1),(1, 15),(15, 15)],
                         RENDER_TYPE = RenderType.SINGLE_IMAGE)

        self.bonus_probability[BonusLife] = (0.5, None)
        self.bonus_probability[BonusMoney] = (0.5, None)
        self.load_map(self.get_tiles_path())
        self.load_items()


    def get_image_path(self):
        return "resources/maps/Level3.png"

    def get_tiles_path(self): #sciezka gdzie jest plik tekstowy opisujacy wyglad mapy
        return "resources/maps/Level3.txt"

    def get_music_path(self):
        return "resources/music/03.MID"

