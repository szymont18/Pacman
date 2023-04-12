from abc import ABC, abstractmethod
from Maps import Tile
from Maps.Tile import *
from Parsers.TileTypeParse import *
from Items.Item import *
import pygame


class GameMap(ABC):
    def __init__(self, MAX_COL, MAX_ROW, FIELD_SIZE, PACMAN_SPAWN_X, PACMAN_SPAWN_Y,POSSIBLE_MONSTERS,MONSTER_SPAWN_TILES, ONLOAD_SPAWN_MONSTERS):
        self.MAX_COL = MAX_COL
        self.MAX_ROW = MAX_ROW

        self.FIELD_SIZE = FIELD_SIZE

        self.PACMAN_SPAWN_X = PACMAN_SPAWN_X
        self.PACMAN_SPAWN_Y = PACMAN_SPAWN_Y

        self.TILES = [[None for __ in range(self.MAX_COL)] for _ in range(self.MAX_ROW)]
        self.TILES[0][5] = 5

        self._items = dict()
        self.bonus_probability = dict()

        self.MONSTER_SPAWN_TILES = MONSTER_SPAWN_TILES #pola na ktorych moga sie zrespic przeciwnicy
        self.POSSIBLE_MONSTERS = POSSIBLE_MONSTERS
        self.ONLOAD_SPAWN_MONSTERS = ONLOAD_SPAWN_MONSTERS #potwory ktore maja sie zrespic na starcie gry (nie sa losowane tylko narzucone z gory)

        self._total_dots = -1 #To niby jest stala ale nie da sie jej ustawic w czasie inicjalizacji wiec ostatecznie nie jest stala

        # Do rysowania
        self._void_image = pygame.transform.scale(pygame.image.load("resources/tiles/void.png"),
                                                  (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self._wall_image = pygame.transform.scale(pygame.image.load("resources/tiles/wall.png"),
                                                  (self.FIELD_SIZE, self.FIELD_SIZE)).convert()

    def set_total_dots(self,total_dots):
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

    #zaladowanie mapy z pliku (Metoda wykonuje sie tylko raz w trakcie inicjalizacji mapy)
    def load_map(self,filePath : str):
        file = open(filePath, 'r')
        row = 0
        col = 0
        pos_x = self.FIELD_SIZE * col
        pos_y = self.FIELD_SIZE * row
        for line in file:
            for number in line.split():
                number_int = int(number)
                self.TILES[row][col] = Tile(TileTypeParser.parse(number_int), pos_x, pos_y)
                col += 1
            if col > self.MAX_COL-1:
                row += 1
                col = 0
        file.close()

        #TE PETLE PONIZEJ NADAJA SIE DO SMIECI
        for i in range(self.MAX_ROW):
            row = i
            for j in range(self.MAX_COL):
                col = j

                if row-1 >= 0 and  self.TILES[row-1][col].COLLISION == False:
                    self.TILES[row][col].add_possible_turn(Direction.UP)
                if row < self.MAX_ROW -1 and self.TILES[row+1][col].COLLISION == False:
                    self.TILES[row][col].add_possible_turn(Direction.DOWN)
                if col -1 >= 0 and self.TILES[row][col-1].COLLISION == False:
                    self.TILES[row][col].add_possible_turn(Direction.LEFT)
                if col < self.MAX_COL - 1 and self.TILES[row][col+1].COLLISION == False:
                    self.TILES[row][col].add_possible_turn(Direction.RIGHT)




    #Klasy dziedziczace w tym miejscu ustawiaja przedmioty na mapie (kropki, bonusy itp)
    @abstractmethod
    def load_items(self):
        pass

    def get_collision_status(self, row: int, col: int):
        row = row % self.MAX_ROW
        col = col % self.MAX_COL
        return self.TILES[row][col].COLLISION

    def get_items(self):
        return self._items

    def remove_item(self,item : Item):
        # para = PairRowCol(item.POS_Y/self.FIELD_SIZE, item.POS_X/self.FIELD_SIZE)

        item_coord = (item.POS_Y / self.FIELD_SIZE, item.POS_X/self.FIELD_SIZE)

        if item_coord in self._items:
            self._items.pop(item_coord)

    def add_item(self, item: Item):
        item_coord = (item.POS_Y / self.FIELD_SIZE, item.POS_X / self.FIELD_SIZE)
        self._items[item_coord] = item

    def get_possible_turns_on(self,row,col):
        if row<0 or row == self.MAX_ROW or col<0 or col == self.MAX_COL:
            print("GameMap/get_possible_turns : lokalizacja poza mapa")
            return []

        return self.TILES[row][col].get_possible_turns()

    def get_onload_monsters(self):
        return self.ONLOAD_SPAWN_MONSTERS






