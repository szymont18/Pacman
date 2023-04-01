from abc import ABC, abstractmethod
from Maps import Tile
from Maps.Tile import Tile
from Parsers.TileTypeParse import *
from Items.Item import *
from Utility.PairRowCol import *

class GameMap(ABC):
    def __init__(self,MAX_COL,MAX_ROW,FIELD_SIZE,PACMAN_SPAWN_X,PACMAN_SPAWN_Y):
        self.MAX_COL = MAX_COL
        self.MAX_ROW = MAX_ROW
        self.FIELD_SIZE = FIELD_SIZE
        self.PACMAN_SPAWN_X = PACMAN_SPAWN_X
        self.PACMAN_SPAWN_Y = PACMAN_SPAWN_Y
        self._TILES = [[None for __ in range(self.MAX_COL)] for _ in range(self.MAX_ROW)]
        self._TILES[0][5] = 5
        self._items = dict()


    def get_pacman_spawn_x(self):
        return self.PACMAN_SPAWN_X

    def get_pacman_spawn_y(self):
        return self.PACMAN_SPAWN_Y

    @abstractmethod
    def get_image_path(self):
        pass

    #zaladowanie mapy z pliku

    def load_map(self,filePath : str):
        file = open(filePath, 'r')
        row = 0
        col = 0
        pos_x = self.FIELD_SIZE * col
        pos_y = self.FIELD_SIZE * row
        for line in file:
            for number in line.split():
                number_int = int(number)
                self._TILES[row][col] = Tile(TileTypeParser.parse(number_int),pos_x,pos_y)
                col+=1
            if col > self.MAX_COL-1:
                row+=1
                col = 0
        file.close()


    #Klasy dziedziczace w tym miejscu ustawiaja przedmioty na mapie (kropki, bonusy itp)
    @abstractmethod
    def load_items(self):
        pass

    def get_collision_status(self, row:int, col:int):
        # if row < 0 or row > self.MAX_ROW or col < 0 or col > self.MAX_COL:
        #     raise Exception("Wspolrzedne poza mapa w get_collision_status")
        return self._TILES[row][col].COLLISION

    def get_items(self):
        return self._items

    def remove_item(self,item : Item):
        para = PairRowCol(item.POS_Y/self.FIELD_SIZE, item.POS_X/self.FIELD_SIZE)

        if self._items.__contains__(para):
            self._items.pop(para)





