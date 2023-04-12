
import pygame

from Enums.SceneTypes import SceneTypes
from gui.Menu.Components.Scene import Scene
from gui.Menu.Scenes.ExitScene import ExitScene
from gui.Menu.Scenes.LeaderScene import LeaderScene
from gui.Menu.Scenes.LevelCreatorScene import LevelCreatorScene
from gui.Menu.Scenes.MainMenuScene import MainMenuScene
from gui.Menu.Scenes.SettingsScene import SettingsScene


class Menu:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height

        # Screen
        self.screen = screen

        # Background
        self.background_image = pygame.transform.scale(pygame.image.load('bg.bmp'), (self.width, self.height))
        self.scenes = [MainMenuScene(self.screen), None, LevelCreatorScene(self.screen), None, LeaderScene(self.screen),
                       SettingsScene(self.screen), ExitScene(self.screen)]

    def draw(self, mouse):
        pygame.draw.rect(self.screen, 'black', [0, 0, self.width, self.height])
        self.screen.blit(self.background_image, (0, 0))
        self.scenes[SceneTypes.to_int(Scene.MENU_SCENE)].draw(mouse)


pygame.init()
screen = pygame.display.set_mode([714, 798])


menu = Menu(714, 798, screen)
fps = 60
timer = pygame.time.Clock()

run = True
mousemotion_event = None
while run:
    timer.tick(fps)
    menu.draw(mousemotion_event)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            mousemotion_event = event
        else: mousemotion_event = None

    pygame.display.flip()

pygame.quit()





