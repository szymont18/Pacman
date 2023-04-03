from abc import abstractmethod
from MapElements.Pacman import Pacman


class Item:
    def __init__(self,POS_X,POS_Y,MAX_SPRITE_NR,SOLID_AREA, is_active=True):
        #atrybuty przedmiotow moga byc publiczne bo i tak sa stale
        self.POS_X = POS_X
        self.POS_Y = POS_Y
        self.sprite_nr = 1
        self.MAX_SPRITE_NR = MAX_SPRITE_NR
        self.SOLID_AREA = SOLID_AREA
        self.is_active = is_active

    @abstractmethod
    def get_image_path(self): #abstract
        pass

    def set_activity(self, new):
        self.is_active = new
