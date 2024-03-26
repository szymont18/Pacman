from ..Enums.TileType import TileType
from ..Items.Dot import Dot
from ..Items.RedBall import RedBall
from ..Maps.GameMap import GameMap
from ..Items.BonusLife import BonusLife
from ..Items.BonusMoney import BonusMoney
from ..Enums.MonsterTypes import *
import pygame
from ..Enums.RenderType import *
from ..Parsers.MapParser import MapParser


class UserLevel(GameMap):
    def __init__(self, field_size, pathname):

        self.map_parser = MapParser(pathname)
        MAX_ROW, MAX_COL, FIELD_SIZE, PACMAN_X, PACMAN_Y, POSSIBLE_MONSTERS, MONSTER_TILES, ONLOAD_MONSTERS, \
            RED_DOTS, TILES, WHITE_DOTS, BONUS_PROBABILITY = self.map_parser.get_all_params()

        RENDERTYPE = RenderType.TILE_BY_TILE
        if MAX_ROW > 17 or MAX_COL > 17:
            RENDERTYPE = RenderType.PACMAN_CENTERED

        super().__init__(MAX_ROW=MAX_ROW,
                         MAX_COL=MAX_COL,
                         FIELD_SIZE=field_size,
                         PACMAN_SPAWN_X=PACMAN_X * field_size,
                         PACMAN_SPAWN_Y=PACMAN_Y * field_size,
                         POSSIBLE_MONSTERS=POSSIBLE_MONSTERS,
                         MONSTER_SPAWN_TILES=MONSTER_TILES,
                         ONLOAD_SPAWN_MONSTERS=ONLOAD_MONSTERS,
                         RED_DOT_POSITIONS=RED_DOTS,
                         RENDER_TYPE=RENDERTYPE)
        self.TILES = TILES
        self.load_white_dots(WHITE_DOTS)
        self.bonus_probability = BONUS_PROBABILITY

    def load_white_dots(self, WHITE_DOTS):

        for (row, col) in WHITE_DOTS:
            para = (row, col)
            self._items[para] = Dot(col * self.FIELD_SIZE, row * self.FIELD_SIZE, self)

        self.set_total_dots(len(self._items.keys()) -
                            len(self.RED_DOT_POSITIONS))  # The number of white dots is described by this equation

        for para in self.RED_DOT_POSITIONS:
            if para in self._items: self._items.pop(para)  # Removing the white dot
            self._items[para] = RedBall(para[1] * self.FIELD_SIZE, para[0] * self.FIELD_SIZE,
                                        self)  # Insert Red Dot

    def get_image_path(self):
        return "resources/maps/Level1.png"

    def get_music_path(self):
        return "resources/music/01.MID"