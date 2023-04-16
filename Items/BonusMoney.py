from Items.Item import Item
import pygame

class BonusMoney(Item):
    def __init__(self,POS_X,POS_Y, probability):
        SOLID_AREA = pygame.Rect(23,23,2,2)
        Item.__init__(self,POS_X,POS_Y,1,SOLID_AREA, False)
        self.probability = probability

    def get_image_path(self):
        return f'resources/items/BonusMoney{self.sprite_nr}.png'

    def __str__(self):
        print(f"BM: {self.POS_Y/48} {self.POS_X/48} ")

    def update(self):
        if pygame.time.get_ticks() - self._blink_timer > self.BLINK_TIME:
            self.sprite_nr = (self.sprite_nr + 1) % 3
            self.sprite_nr = self.sprite_nr if self.sprite_nr != 0 else 1
            self._blink_timer = pygame.time.get_ticks()