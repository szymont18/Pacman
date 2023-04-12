from Items.Item import Item
import pygame


class Dot(Item):
    def __init__(self,POS_X,POS_Y):
        SOLID_AREA = pygame.Rect(23,23,2,2)
        Item.__init__(self,POS_X,POS_Y,1,SOLID_AREA)

    def get_image_path(self):
        return "resources/items/Dot.png"

    def __str__(self):
        print(f"DOT: {self.POS_Y/48} {self.POS_X/48} ")
