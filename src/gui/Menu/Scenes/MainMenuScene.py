from src.Enums.SceneTypes import SceneTypes
from src.MapElements.Vector2d import Vector2d
from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *
import pygame


class MainMenuScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        # Rectangles button
        self.start_game_button = None
        self.create_level_button = None
        self.leader_board_button = None
        self.instructions = None
        self.setting = None
        self.exit = None

        # Texts
        self.title = None

        start_button = Button(Vector2d(350, 250), 214, 50, "Start Game", screen,
                              lambda: Scene.change_menu_scene(SceneTypes.START))
        create_level = Button(Vector2d(400, 250), 214, 50, "Create Level", screen,
                              lambda : Scene.change_menu_scene(SceneTypes.LEVEL_CREATOR))
        leader_board = Button(Vector2d(450, 250), 214, 50, "Leader_board", screen,
                              lambda: Scene.change_menu_scene(SceneTypes.LEADER))
        settings = Button(Vector2d(500, 250), 214, 50, "Settings", screen,
                          lambda: Scene.change_menu_scene(SceneTypes.SETTINGS))
        instructions = Button(Vector2d(550, 250), 214, 50, "Instructions", screen,
                              lambda : Scene.change_menu_scene(SceneTypes.INSTRUCTIONS))
        exit_button = Button(Vector2d(600, 250), 214, 50, "Exit", screen,
                             lambda : Scene.change_menu_scene(SceneTypes.EXIT))

        title_text = TextArea(Vector2d(200, 200), 314, 100, "P a c m a n", screen)

        self.set_buttons(start_button, create_level, leader_board, settings, instructions, exit_button)
        self.set_texts(title_text)

    def draw(self, mouse):
        self.title.draw()

        self.start_game_button.draw()
        self.create_level_button.draw()
        self.leader_board_button.draw()
        self.setting.draw()
        self.instructions.draw()
        self.exit.draw()

        self.start_game_button.is_clicked(mouse)
        self.create_level_button.is_clicked(mouse)
        self.leader_board_button.is_clicked(mouse)
        self.setting.is_clicked(mouse)
        self.instructions.is_clicked(mouse)
        self.exit.is_clicked(mouse)

    def set_buttons(self, start_game_button, create_level_button, leader_board_button,
                    setting, instructions, exit_button):
        self.start_game_button = start_game_button
        self.create_level_button = create_level_button
        self.leader_board_button = leader_board_button
        self.setting = setting
        self.instructions = instructions
        self.exit = exit_button

    def set_texts(self, title: TextArea):
        self.title = title