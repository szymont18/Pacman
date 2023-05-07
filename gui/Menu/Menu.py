
import pygame

from Enums.SceneTypes import SceneTypes
from gui.Menu.Components.Scene import Scene
from gui.Menu.Scenes.ExitScene import ExitScene
from gui.Menu.Scenes.InstructionScene import InstructionScene
from gui.Menu.Scenes.LeaderScene import LeaderScene
from gui.Menu.Scenes.LevelCreatorScene import LevelCreatorScene
from gui.Menu.Scenes.MainMenuScene import MainMenuScene
from gui.Menu.Scenes.SettingsScene import SettingsScene
from gui.Menu.Scenes.StartGameScene import StartGameScene


class Menu:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height

        # Screen
        self.screen = screen

        # Background
        self.background_image = pygame.transform.scale(pygame.image.load("resources/ORIGINAL/LEVELS/Level01.bmp"),
                                                       (self.width, self.height))
        self.scenes = [MainMenuScene(self.screen), StartGameScene(self.screen), LevelCreatorScene(self.screen),
                       InstructionScene(self.screen), LeaderScene(self.screen), SettingsScene(self.screen),
                       ExitScene(self.screen)]

    def draw(self, mouse):
        pygame.draw.rect(self.screen, 'black', [0, 0, self.width, self.height])
        self.screen.blit(self.background_image, (0, 0))
        self.scenes[SceneTypes.to_int(Scene.MENU_SCENE)].draw(mouse)








