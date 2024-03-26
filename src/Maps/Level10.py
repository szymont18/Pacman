from ..Maps.GameMap import GameMap
from ..Items.Slow import Slow
from ..Enums.MonsterTypes import *
from ..Items.BonusLife import BonusLife
from ..Items.Nuke import Nuke
from ..Items.BonusMoney import BonusMoney
from ..Enums.RenderType import *

class Level10(GameMap):
    def __init__(self,field_size):
        super().__init__(MAX_ROW = 17,
                         MAX_COL = 17,
                         FIELD_SIZE = field_size,
                         PACMAN_SPAWN_X=field_size * 8,
                         PACMAN_SPAWN_Y=field_size * 13,
                         POSSIBLE_MONSTERS=[MonsterTypes.DEMON],
                         MONSTER_SPAWN_TILES=[(8, 8)],
                         ONLOAD_SPAWN_MONSTERS=[(MonsterTypes.DEMON,(8,8))],
                         RED_DOT_POSITIONS=[(7, 7),(9, 9),(7,9),(9,7)],
                         RENDER_TYPE=RenderType.SINGLE_IMAGE)

        self.bonus_probability[Slow] = (0.2, None)
        self.bonus_probability[BonusLife] = (0.3, None)
        self.bonus_probability[Nuke] = (0.5, None)

        self.load_map(self.get_tiles_path())
        self.load_items()


    def get_image_path(self):
        return "resources/maps/Level10.png"

    def get_tiles_path(self): #sciezka gdzie jest plik tekstowy opisujacy wyglad mapy
        return "resources/maps/Level10.txt"

    def get_music_path(self):
        return "resources/music/08.MID"
