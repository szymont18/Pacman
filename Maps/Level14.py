from Maps.GameMap import GameMap
from Items.Slow import Slow
from Enums.MonsterTypes import *
from Items.BonusLife import BonusLife
from Items.Nuke import Nuke
from Items.BonusMoney import BonusMoney
from Enums.RenderType import *

class Level14(GameMap):
    def __init__(self,field_size):
        super().__init__(MAX_ROW = 34,
                         MAX_COL = 34,
                         FIELD_SIZE = field_size,
                         PACMAN_SPAWN_X=field_size * 8,
                         PACMAN_SPAWN_Y=field_size * 11,
                         POSSIBLE_MONSTERS=[MonsterTypes.SKULL],
                         MONSTER_SPAWN_TILES=[(5, 8),(5,24),(21,8),(21,24)],
                         ONLOAD_SPAWN_MONSTERS=[(MonsterTypes.DEMON,(8,8)),(MonsterTypes.SKULL,(8,24)),
                                                (MonsterTypes.SKULL,(24,8)),(MonsterTypes.SKULL,(24,24))],
                         RED_DOT_POSITIONS=[(7,7),(9,9),(7,24),(9,26),(24,24),(26,26),(24,7),(26,9)],
                         RENDER_TYPE=RenderType.PACMAN_CENTERED)

        #self.bonus_probability[BonusLife] = (0.4, None)
        #self.bonus_probability[BonusMoney] = (0.2, None)
        self.bonus_probability[Slow] = (0.4, None)
        self.bonus_probability[BonusLife] = (0.4, None)
        self.bonus_probability[Nuke] = (0.1, None)
        self.bonus_probability[BonusMoney] = (0.1, None)

        self.load_map(self.get_tiles_path())
        self.load_items()


    def get_image_path(self):
        return "resources/maps/Level14.png"

    def get_tiles_path(self): #sciezka gdzie jest plik tekstowy opisujacy wyglad mapy
        return "resources/maps/Level14.txt"

    def get_music_path(self):
        return "resources/music/20.MID"
