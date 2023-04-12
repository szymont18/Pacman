from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *
import pygame


class SettingsScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        self.rectangle_window = pygame.rect.Rect((100, 200), (514, 450))
        self.title = TextArea((200, 200), 314, 100, "Settings", self.screen, rgb=(247, 245, 245))
        self.sound_text = TextArea((285, 200), 314, 100, "Sound", self.screen, rgb=(247, 245, 245), font_size=30)

        self.return_button = Button((600, 100), 100, 100, "Return", screen,
                                    lambda: Scene.change_menu_scene(SceneTypes.MAIN))

    def draw(self, mouse):
        pygame.draw.rect(self.screen, 'black', self.rectangle_window)
        self.title.draw()
        self.sound_text.draw()
        self.return_button.draw()

        self.return_button.is_clicked(mouse)





