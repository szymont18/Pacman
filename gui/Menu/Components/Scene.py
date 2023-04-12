import pygame
from abc import ABC, abstractmethod
from Enums.SceneTypes import *

class Scene:
    MENU_SCENE = SceneTypes.MAIN
    REACTION_TIME = -float('inf')
    def __init__(self, screen):
        self.screen = screen

    @abstractmethod
    def draw(self, mouse):
        pass

    @staticmethod
    def change_menu_scene(new_scene):
        if pygame.time.get_ticks() - Scene.REACTION_TIME < 500: return
        Scene.REACTION_TIME = pygame.time.get_ticks()
        Scene.MENU_SCENE = new_scene
