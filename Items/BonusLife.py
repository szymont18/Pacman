from Items.Item import Item
import pygame

class BonusLife(Item):
    def __init__(self,POS_X,POS_Y, probability,MAP):
        SOLID_AREA = pygame.Rect(23,23,2,2)
        Item.__init__(self,POS_X,POS_Y,2,SOLID_AREA,MAP,4)
        self.probability = probability

    def get_image_path(self):
        if not self._is_eaten:
            return f'resources/items/BonusLife{self._sprite_nr}.png'
        else:
            return f'resources/items/1UP_{self._sprite_nr}.png'

        # else:
        #     return f'resources/items/RedBall1.png'
    def __str__(self):
        print(f"BL: {self.POS_Y/48} {self.POS_X/48} ")

