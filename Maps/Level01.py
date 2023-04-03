from Maps.GameMap import GameMap
from Enums import TileType
from Enums.TileType import TileType
from Utility.PairRowCol import PairRowCol
from Items.Dot import Dot
from Items.RedBall import RedBall
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
                    para = PairRowCol(i,j)
                    self._items[para] = Dot(j*self.FIELD_SIZE,i*self.FIELD_SIZE)
        redDotPositions = [PairRowCol(1,1),
                           PairRowCol(10,1),
                           PairRowCol(15,1),
                           PairRowCol(1,15),
                           PairRowCol(10,15),
                           PairRowCol(15,15)]

        for para in redDotPositions:
            self._items.pop(para) #usuwamy kropke ktora tam byla
            self._items[para] = RedBall(para.COL*self.FIELD_SIZE, para.ROW*self.FIELD_SIZE) #wkladamy na jej miejsce RedBall


