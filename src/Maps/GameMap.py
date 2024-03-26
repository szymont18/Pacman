import random
from abc import ABC, abstractmethod
from ..Maps import Tile
from ..Maps.Tile import *
from ..Parsers.TileTypeParse import *
from ..Items.Item import *
import pygame
from ..Items.Dot import Dot
from ..Items.RedBall import RedBall


class GameMap(ABC):
    def __init__(self, MAX_ROW, MAX_COL, FIELD_SIZE, PACMAN_SPAWN_X, PACMAN_SPAWN_Y,
                 POSSIBLE_MONSTERS, MONSTER_SPAWN_TILES, ONLOAD_SPAWN_MONSTERS,RED_DOT_POSITIONS,RENDER_TYPE,PORTALS = None):
        self.MAX_ROW = MAX_ROW
        self.MAX_COL = MAX_COL


        self.FIELD_SIZE = FIELD_SIZE

        self.PACMAN_SPAWN_X = PACMAN_SPAWN_X
        self.PACMAN_SPAWN_Y = PACMAN_SPAWN_Y

        self.TILES = [[None for __ in range(self.MAX_COL)] for _ in range(self.MAX_ROW)]
        #self.TILES[0][5] = 5

        self._items = dict() #Dict for all items (dots,keys...)
        self.bonus_probability = dict()
        self.__void_places = {}

        self.MONSTER_SPAWN_TILES = MONSTER_SPAWN_TILES  # Tiles where monsters can spawn
        self.POSSIBLE_MONSTERS = POSSIBLE_MONSTERS
        self.ONLOAD_SPAWN_MONSTERS = ONLOAD_SPAWN_MONSTERS  # Monsters that spawn when game starts
        #self.PORTALS = PORTALS

        self.RED_DOT_POSITIONS = RED_DOT_POSITIONS
        self._total_dots = -1  # It's supposed to be a constant, but it can't be set during initialization,
        # so it's not a constant in the end

        # Should map be drawn tile by tile or just 1 image (Tile by tile is meant to be for custom maps and big maps)
        self.RENDER_TYPE = RENDER_TYPE

    def set_total_dots(self, total_dots):
        self._total_dots = total_dots

    def get_pacman_spawn_x(self):
        return self.PACMAN_SPAWN_X

    def get_pacman_spawn_y(self):
        return self.PACMAN_SPAWN_Y

    def get_total_dots(self):
        return self._total_dots

    @abstractmethod
    def get_image_path(self):
        pass

    @abstractmethod
    def get_music_path(self):
        pass

    # zaladowanie mapy z pliku (Metoda wykonuje sie tylko raz w trakcie inicjalizacji mapy)
    def load_map(self, filePath: str):
        file = open(filePath, 'r')
        row = 0
        col = 0
        pos_x = self.FIELD_SIZE * col
        pos_y = self.FIELD_SIZE * row
        for line in file:
            for number in line.split():
                number_int = int(number)
                self.TILES[row][col] = Tile(TileTypeParser.parse(number_int), pos_x, pos_y)
               # print(row, col,self.TILES[row][col])
                col += 1
            if col > self.MAX_COL - 1:
                row += 1
                col = 0
        file.close()
        # Loops below are garbage
        for i in range(self.MAX_ROW):
            row = i
            for j in range(self.MAX_COL):
                col = j

                if row - 1 >= 0 and self.TILES[row - 1][col].COLLISION == False:
                    self.TILES[row][col].add_possible_turn(Direction.UP)
                if row < self.MAX_ROW - 1 and self.TILES[row + 1][col].COLLISION == False:
                    self.TILES[row][col].add_possible_turn(Direction.DOWN)
                if col - 1 >= 0 and self.TILES[row][col - 1].COLLISION == False:
                    self.TILES[row][col].add_possible_turn(Direction.LEFT)
                if col < self.MAX_COL - 1 and self.TILES[row][col + 1].COLLISION == False:
                    self.TILES[row][col].add_possible_turn(Direction.RIGHT)


    def load_items(self):
        for i in range(self.MAX_ROW):
            for j in range(self.MAX_COL):
                if self.TILES[i][j].TYPE == TileType.VOID:
                    para = (i, j)
                    self._items[para] = Dot(j * self.FIELD_SIZE, i * self.FIELD_SIZE, self)

        self.set_total_dots(len(self._items.keys()) -
                            len(self.RED_DOT_POSITIONS))  # The number of white dots is described by this equation

        for para in self.RED_DOT_POSITIONS:
            self._items.pop(para)  # Removing the white dot
            self._items[para] = RedBall(para[1] * self.FIELD_SIZE, para[0] * self.FIELD_SIZE,
                                        self)  # Insert Red Dot

    def get_collision_status(self, row: int, col: int):
        row = row % self.MAX_ROW
        col = col % self.MAX_COL
        return self.TILES[row][col].COLLISION

    def get_items(self):
        return self._items

    def remove_item(self, item: Item):
        # para = PairRowCol(item.POS_Y/self.FIELD_SIZE, item.POS_X/self.FIELD_SIZE)

        item_coord = (item.POS_Y / self.FIELD_SIZE, item.POS_X / self.FIELD_SIZE)

        if item_coord in self._items:
            self._items.pop(item_coord)

        self.__void_places[(item.POS_Y, item.POS_X)] = True

    def item_in_square(self, row, col):
        if (row, col) in self._items: return True
        else: return False

    def add_item(self, item: Item):
        item_coord = (item.POS_Y / self.FIELD_SIZE, item.POS_X / self.FIELD_SIZE)
        self._items[item_coord] = item

        if (item.POS_Y, item.POS_X) in self.__void_places: self.__void_places.pop((item.POS_Y, item.POS_X))

    def get_possible_turns_on(self, row, col):
        if row < 0 or row == self.MAX_ROW or col < 0 or col == self.MAX_COL:
            print("GameMap/get_possible_turns : lokalizacja poza mapa")
            return []

        return self.TILES[row][col].get_possible_turns()

    def get_onload_monsters(self):
        return self.ONLOAD_SPAWN_MONSTERS

    def get_random_spawn_place(self):
        return random.choice(list(self.__void_places.keys()))

    def clear_items(self):
        self._items = dict()
