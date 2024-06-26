
import pygame

from src.Items.Item import Item


class Dot(Item):
    def __init__(self, POS_X, POS_Y, MAP):
        SOLID_AREA = pygame.Rect(5, 5, 22, 22)
        Item.__init__(self, POS_X, POS_Y, 1, SOLID_AREA, MAP, 0)

    def get_image_path(self):
        return "resources/items/Dot.png"

    def get_sound_path(self):
        return "resources/sound/EatDot.wav"

    def __str__(self):
        print(f"DOT: {self.POS_Y/48} {self.POS_X/48} ")