from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *
import pygame


class ExitScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        self.rectangle = pygame.rect.Rect((200, 300), (314, 200))

        self.text = TextArea(Vector2d(300, 200), 314, 100, 'Do you want to exit?', self.screen, font_size=30,
                             rgb=(247, 245, 245))
        self.yes_button = Button(Vector2d(400, 250), 100, 75, 'Yes', self.screen, lambda: exit(0))
        self.no_button = Button(Vector2d(400, 364), 100, 75, 'No', self.screen, lambda : Scene.change_menu_scene(SceneTypes.MAIN))

        self.yes_button.change_cover_colors((196, 191, 37), (204, 6, 6))

    def draw(self, mouse):
        pygame.draw.rect(self.screen, 'black', self.rectangle)
        self.text.draw()
        self.yes_button.draw()
        self.no_button.draw()

        self.yes_button.is_clicked(mouse)
        self.no_button.is_clicked(mouse)


