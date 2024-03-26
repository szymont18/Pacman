import pygame
from abc import ABC, abstractmethod

from src.Enums.SceneTypes import SceneTypes


class Scene:
    MENU_SCENE = SceneTypes.MAIN
    REACTION_TIME = -float('inf')
    SPRITE_TIME = -float('inf')
    GAME_SPEC = None

    def __init__(self, screen):
        self.screen = screen
        self.sprite_nr = 0

    @abstractmethod
    def draw(self, mouse):
        pass

    @staticmethod
    def change_menu_scene(new_scene):
        if pygame.time.get_ticks() - Scene.REACTION_TIME < 500: return
        Scene.REACTION_TIME = pygame.time.get_ticks()
        Scene.MENU_SCENE = new_scene

    def sprite_blink(self):
        if pygame.time.get_ticks() - Scene.SPRITE_TIME < 200: return
        Scene.SPRITE_TIME = pygame.time.get_ticks()
        self.sprite_nr += 1
