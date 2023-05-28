from Maps.GameMap import GameMap
from Items.BonusLife import BonusLife
from Items.BonusMoney import BonusMoney
from Enums.MonsterTypes import *
import pygame
from Enums.RenderType import *

class Level01(GameMap):
    def __init__(self,field_size):

        super().__init__(MAX_ROW = 17,
                         MAX_COL = 17,
                         FIELD_SIZE = field_size,
                         PACMAN_SPAWN_X = field_size * 2,
                         PACMAN_SPAWN_Y = field_size * 10,
                         POSSIBLE_MONSTERS = [MonsterTypes.SKULL],
                         MONSTER_SPAWN_TILES = [(8, 8)],
                         ONLOAD_SPAWN_MONSTERS = [(MonsterTypes.SKULL, (8, 8))],
                         RED_DOT_POSITIONS = [(1, 1),(10, 1),(15, 1),(1, 15), (10, 15),(15, 15)],
                         RENDER_TYPE = RenderType.SINGLE_IMAGE)
                        # PORTALS = [(8,0),(8,16)]) #Portale przenoszace na druga strone mapy (sa jedynie kosmetyczne bo mechanika gry przenosi gracza automatycznie)

        self.load_map(self.get_tiles_path())
        self.load_items()

        self.bonus_probability[BonusLife] = (0.5, None)
        self.bonus_probability[BonusMoney] = (0.5, None)

    def get_image_path(self):
        return "resources/maps/Level1.png"

    def get_tiles_path(self):
        return "resources/maps/Level1.txt"

    def get_music_path(self):
        return "resources/music/01.MID"


