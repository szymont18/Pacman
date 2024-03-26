
import pygame

from src.Items.Item import Item


class RedBall(Item):
    def __init__(self,POS_X,POS_Y,MAP):
        SOLID_AREA = pygame.Rect(5,5,32, 32)
        Item.__init__(self,POS_X,POS_Y,4,SOLID_AREA,MAP,4)

    def get_image_path(self):

        if not self._is_eaten:
            return f'resources/items/RedBall{self._sprite_nr}.png'
        else:
            return f'resources/items/RB_EATEN_{self._sprite_nr}.png'

    def get_sound_path(self):
        return "resources/sound/RedBallEaten.wav"

    def __str__(self):
        print(f"RB: {self.POS_Y/48} {self.POS_X/48} ")

