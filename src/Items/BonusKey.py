import Item
import pygame

class BonusKey(Item):
    def __init__(self, POS_X, POS_Y, probability, MAP):
        SOLID_AREA = pygame.Rect(5,5,32, 32)
        Item.__init__(self, POS_X, POS_Y, 2, SOLID_AREA, MAP, 4)
        self.probability = probability

    def get_image_path(self):
        if not self._is_eaten:
            return f'resources/items/BonusKey{self._sprite_nr}.png'
        else:
            return f'resources/items/PickedKey{self._sprite_nr}.png'

    def get_sound_path(self):
        return "resources/sound/Bonusey.wav"

    def __str__(self):
        print(f"BL: {self.POS_Y / 48} {self.POS_X / 48} ")
