from Maps.GameMap import GameMap
from Enums import TileType
from Enums.TileType import TileType
from Items.Dot import Dot
from Items.RedBall import RedBall
from Items.BonusLife import BonusLife
from Items.BonusMoney import BonusMoney
from Maps.Tile import *


class Level01(GameMap):
    def __init__(self,max_row,max_col,field_size):
        super().__init__(max_row,max_col,field_size,field_size*2,field_size*10)
        self.load_map(self.get_tiles_path())
        self.load_items()


    def get_image_path(self):
        return "resources/maps/Level01.png"

    def get_tiles_path(self): #sciezka gdzie jest plik tekstowy opisujacy wyglad mapy
        return "resources/maps/Level01.txt"

    #Metoda laduje itemy (Dots i Redballs)
    def load_items(self):
        for i in range(self.MAX_ROW):
            for j in range(self.MAX_COL):
                if self.TILES[i][j].TYPE == TileType.VOID:
                    para = (i, j)
                    self._items[para] = Dot(j*self.FIELD_SIZE, i*self.FIELD_SIZE)

        # self._items[(14, 3)] = BonusLife(3 * self.FIELD_SIZE, 14 * self.FIELD_SIZE, 0.5)
        # self._items[(2, 13)] = BonusMoney(13 * self.FIELD_SIZE, 2 * self.FIELD_SIZE, 0.5)

        self.bonus_probability[BonusLife] = (0.5, (3 * self.FIELD_SIZE, 13 * self.FIELD_SIZE))
        self.bonus_probability[BonusMoney] = (0.5, (13 * self.FIELD_SIZE, 3 * self.FIELD_SIZE))

        redDotPositions = [(1, 1),
                           (10, 1),
                           (15, 1),
                           (1, 15),
                           (10, 15),
                           (15, 15)]

        for para in redDotPositions:
            self._items.pop(para) #usuwamy kropke ktora tam byla
            self._items[para] = RedBall(para[1]*self.FIELD_SIZE, para[0]*self.FIELD_SIZE) #wkladamy na jej miejsce RedBall


