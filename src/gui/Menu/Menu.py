
import pygame

from src.Enums.SceneTypes import SceneTypes
from src.gui.Menu.Components.Scene import Scene
from src.gui.Menu.Scenes.ExitScene import ExitScene
from src.gui.Menu.Scenes.InstructionScene import InstructionScene
from src.gui.Menu.Scenes.LeaderScene import LeaderScene
from src.gui.Menu.Scenes.LevelCreatorScene import LevelCreatorScene
from src.gui.Menu.Scenes.MainMenuScene import MainMenuScene
from src.gui.Menu.Scenes.SettingsScene import SettingsScene
from src.gui.Menu.Scenes.StartGameScene import StartGameScene


class Menu:
    def __init__(self, width, height, screen, game_spec):
        self.width = width
        self.height = height

        # Screen
        self.screen = screen

        # Background
        self.background_image = pygame.transform.scale(pygame.image.load("resources/maps/Level1.png"),
                                                       (self.width, self.height))
        self.scenes = [MainMenuScene(self.screen), StartGameScene(self.screen), LevelCreatorScene(self.screen),
                       InstructionScene(self.screen), LeaderScene(self.screen), SettingsScene(self.screen),
                       ExitScene(self.screen)]

        self.game_spec = game_spec

        # Set GAME_SPEC for all scenes
        Scene.GAME_SPEC = game_spec
    def draw(self, mouse):
        pygame.draw.rect(self.screen, 'black', [0, 0, self.width, self.height])
        self.screen.blit(self.background_image, (0, 0))
        self.scenes[SceneTypes.to_int(Scene.MENU_SCENE)].draw(mouse)








