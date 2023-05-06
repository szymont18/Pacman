import pygame
from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *


class LevelCreatorScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        self.text = TextArea(Vector2d(200, 200), 400, 400, "TO DO", screen)
        self.return_button = Button(Vector2d(600, 600), 100, 100, "Return", screen,
                                    lambda: Scene.change_menu_scene(SceneTypes.MAIN))

    def draw(self, mouse):
        self.text.draw()
        self.return_button.draw()

        self.return_button.is_clicked(mouse)



