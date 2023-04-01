from abc import abstractmethod


class Item:

    def __init__(self,POS_X,POS_Y,MAX_SPRITE_NR,SOLID_AREA):
        #atrybuty przedmiotow moga byc publiczne bo i tak sa stale
        self.POS_X = POS_X
        self.POS_Y = POS_Y
        self.sprite_nr = 1
        self.MAX_SPRITE_NR = MAX_SPRITE_NR
        self.SOLID_AREA = SOLID_AREA

    @abstractmethod
    def get_image_path(self): #abstract
        pass

