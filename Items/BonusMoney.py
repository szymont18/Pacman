from Items.Item import Item
import pygame

class BonusMoney(Item):
    def __init__(self,POS_X,POS_Y, probability):
        SOLID_AREA = pygame.Rect(23,23,2,2)
        Item.__init__(self,POS_X,POS_Y,1,SOLID_AREA, False)
        self.probability = probability

    def get_image_path(self):
        return "resources/items/BonusMoney"+str(self.sprite_nr)+".png"

    def __str__(self):
        print(f"BM: {self.POS_Y/48} {self.POS_X/48} ")