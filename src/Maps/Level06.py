from Maps.GameMap import GameMap
from Items.BonusLife import BonusLife
from Items.BonusMoney import BonusMoney
from Items.Slow import Slow
from Enums.MonsterTypes import *
from Enums.RenderType import *

class Level06(GameMap):
    def __init__(self,field_size):
        super().__init__(MAX_ROW = 17,
                         MAX_COL = 17,
                         FIELD_SIZE = field_size,
                         PACMAN_SPAWN_X=field_size * 1,
                         PACMAN_SPAWN_Y=field_size * 15,
                         POSSIBLE_MONSTERS=[MonsterTypes.SKULL],
                         MONSTER_SPAWN_TILES=[(1, 1)],
                         ONLOAD_SPAWN_MONSTERS=[(MonsterTypes.SKULL,(1,1)),(MonsterTypes.GHOST,(1,15)),(MonsterTypes.GHOST,(15,15))],
                         RED_DOT_POSITIONS=[(3, 13),(5, 11),(7,9),(7,8),(7,7),(8,7),(8,8),(8,9),(9,7),(9,8),(9,9),
                           (11 , 5),(13 , 3),(15 , 15)],
                         RENDER_TYPE=RenderType.SINGLE_IMAGE)

        self.bonus_probability[BonusLife] = (0.4, None)
        self.bonus_probability[BonusMoney] = (0.2, None)
        self.bonus_probability[Slow] = (0.4, None)
        self.load_map(self.get_tiles_path())
        self.load_items()


    def get_image_path(self):
        return "resources/maps/Level6.png"

    def get_tiles_path(self): #sciezka gdzie jest plik tekstowy opisujacy wyglad mapy
        return "resources/maps/Level6.txt"

    def get_music_path(self):
        return "resources/music/06.MID"
