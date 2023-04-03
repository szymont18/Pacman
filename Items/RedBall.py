from Items.Item import Item
import pygame


class RedBall(Item):
    def __init__(self,POS_X,POS_Y):
        SOLID_AREA = pygame.Rect(23,23,2,2)
        Item.__init__(self,POS_X,POS_Y,4,SOLID_AREA)

    def get_image_path(self):
        return "resources/items/RedBall"+str(self.sprite_nr)+".png"
