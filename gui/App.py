import time
from time import sleep

import pygame.time

from Enums.SceneTypes import SceneTypes
from MapElements.Vector2d import Vector2d
from Utility.GameSpec import GameSpec
from gui.Menu.Components.Scene import Scene
from gui.Menu.Components.TextArea import TextArea
from gui.Menu.Menu import Menu
from gui.Menu.Scenes.LevelStatusScene import LevelStatusScene, STATUS
from gui.TextureFactory import *
from Utility.Engine import *
from MapElements.MapElement import *
from Maps.GameMap import *
from Maps.Level01 import *
from Maps.Level02 import *
from Maps.Level03 import *
from Maps.Level04 import *
from Maps.Level05 import *
from Maps.Level06 import *
from Enums.TileType import *
from enum import Enum


class APPEVENT(Enum):
    MENU = 0
    GAME = 1
    GAME_STATUS = 2


class App:
    def __init__(self):

        # Init pygame
        pygame.init()

        self.__TEXTURE_FACTORY = TextureFactory()
        # This value will be parameterized in the future
        self.MAX_ROW = 17
        self.MAX_COL = 17
        self.FIELD_SIZE = 42

        # Place for future scene (MENU...)

        # Window (screen)
        self.window = pygame.display.set_mode((self.MAX_COL * self.FIELD_SIZE, (self.MAX_ROW + 2) * self.FIELD_SIZE))

        # FONT
        pygame.font.init()
        self.font = pygame.font.SysFont(None, self.FIELD_SIZE)  # None is okey there

        # LISTENER
        self.__KEYH = KeyHandler()

        # setMenuScene() Method render menu
        # setGameScene() Method render game button

        # In the future in Menu there will be a button which will launch the game
        self.GAME_SPEC = GameSpec()
        self.menu = Menu(714, 798, self.window, self.GAME_SPEC)
        self.level_status_scene = LevelStatusScene(self.window)

        # Run and mouse event's
        self.KEEP_RUNNING = True
        self.event = None
        self.fps = 60
        self.timer = pygame.time.Clock()

        # Launch game
        self.app_event = APPEVENT.MENU
        self.game_response = None

        self.launch_app()

    # Clear window
    def clear_map(self):
        self.window.fill((0, 0, 0))

    # Draw pacman and monsters
    def draw_map_element(self, element: MapElement):
        pos_x = element.get_pos_x()
        pos_y = element.get_pos_y()

        image = self.__TEXTURE_FACTORY.load(element.get_image_path())
        image_adjusted = pygame.transform.scale(image, (self.FIELD_SIZE, self.FIELD_SIZE))
        self.window.blit(image_adjusted, (pos_x, pos_y))

    def draw_map(self, game_map: GameMap):
        # image = self.__TEXTURE_FACTORY.load(map.get_image_path())
        # image_adjusted = pygame.transform.scale(image,
        # (self.FIELD_SIZE * self.MAX_ROW, self.FIELD_SIZE * self.MAX_COL))
        # self.window.blit(image_adjusted, (0, 0))

        for row in range(self.MAX_ROW):
            for col in range(self.MAX_COL):
                x, y = col * self.FIELD_SIZE, row * self.FIELD_SIZE
                if game_map.TILES[row][col].TYPE == TileType.WALL:
                    self.window.blit(game_map.get_wall_image(), (x, y))
                else:
                    self.window.blit(game_map.get_void_image(), (x, y))

    def draw_items(self, game_map: GameMap):
        items = game_map.get_items()
        # keys_to_removed = []

        for key in items.keys():
            # print(key.ROW,key.COL)
            item = items.get(key)
            # if item.is_active:
            image = self.__TEXTURE_FACTORY.load(item.get_image_path())
            image_adjusted = pygame.transform.scale(image, (self.FIELD_SIZE, self.FIELD_SIZE))
            self.window.blit(image_adjusted, (item.POS_X, item.POS_Y))

            # Engine remembers about clearing their stuff
            # else:
            #    keys_to_removed.append(key)

        # for key in keys_to_removed:
        #    items.pop(key)

    def draw_pacman_status(self, lives_number: int, score_number: int):
        start_hearth_position = (10, self.MAX_ROW * self.FIELD_SIZE)  # OFFSET (should be parametrized ?) (???)
        # print("Draw pacman status", lives_number, score_number)
        for i in range(min(lives_number, 5)):  # MAX 5 lives can be showed
            self.window.blit(self.__TEXTURE_FACTORY.load("resources/items/BonusLife1.png"), start_hearth_position)
            start_hearth_position = (start_hearth_position[0] + self.FIELD_SIZE, start_hearth_position[1])

        if lives_number > 5:
            img = self.font.render("...", True, "white")
            self.window.blit(img, start_hearth_position)

        score_img = self.font.render("SCORE: " + str(score_number), True, "white")
        self.window.blit(score_img, (self.MAX_COL * (self.FIELD_SIZE - 15), self.MAX_ROW * self.FIELD_SIZE))

    #
    # def draw_win_level(self):
    #     self.level_status_scene.change_game_status(STATUS.LVL_WIN)
    #     self.level_status_scene.draw(None)
    #
    # def draw_lose_level(self):
    #     self.level_status_scene.change_game_status(STATUS.LVL_LOSE)
    #     self.level_status_scene.draw(None)
    #
    # def draw_game_win(self):
    #     pass

    def draw_menu(self):
        self.menu.draw(None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.KEEP_RUNNING = False
            elif event.type == pygame.MOUSEMOTION:
                self.event = event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.event = event
            else:
                self.event = None

            self.menu.draw(self.event)

    def launch_game(self):
        # Game
        response = None
        level_id = None

        level_id = self.GAME_SPEC.get_level_to_play()
        hardness = self.GAME_SPEC.get_hardness()  # Should do sth to change hardness of the game (number of enemies)            # TODO After map parsing

        game_map = None
        if level_id == 0:
            game_map = Level01(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)
        elif level_id == 1:
            game_map = Level02(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)
        elif level_id == 2:
            game_map = Level03(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)
        elif level_id == 3:
            game_map = Level04(self.MAX_ROW,self.MAX_COL,self.FIELD_SIZE)
        elif level_id == 4:
            game_map = Level05(self.MAX_ROW,self.MAX_COL,self.FIELD_SIZE)
        elif level_id == 5:
            game_map = Level06(self.MAX_ROW,self.MAX_COL,self.FIELD_SIZE)

        else:
            return -1

        engine = Engine(game_map, self.MAX_ROW, self.MAX_COL, self, self.__KEYH, self.FIELD_SIZE,
                            self.GAME_SPEC)
        return engine.run()

    def draw_status(self, game_response, level_id):
        self.clear_map()
        if game_response is not None:
            self.GAME_SPEC.set_start_game(False)

        if game_response == STATUS.LVL_WIN and level_id == 5:
            self.level_status_scene.change_game_status(STATUS.GAME_WIN)

        elif game_response == STATUS.LVL_WIN and level_id < 5:
            self.level_status_scene.change_game_status(STATUS.LVL_WIN)

        elif game_response == STATUS.LVL_LOSE:
            self.level_status_scene.change_game_status(STATUS.LVL_LOSE)

        self.level_status_scene.draw(None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.KEEP_RUNNING = False

            self.level_status_scene.draw(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                if self.level_status_scene.status == STATUS.LVL_WIN:
                    self.GAME_SPEC.increment_lvl()
                    self.app_event = APPEVENT.GAME

                else:
                    self.GAME_SPEC.reset()
                    self.app_event = APPEVENT.MENU

    def launch_app(self):
        # Menu and GameStatus
        while self.KEEP_RUNNING:
            self.timer.tick(self.fps)

            # Menu
            if self.app_event == APPEVENT.MENU:
                self.draw_menu()

                self.app_event = APPEVENT.GAME if self.GAME_SPEC.get_start_game_status() else APPEVENT.MENU

            elif self.app_event == APPEVENT.GAME:
                game_time = time.time()
                self.game_response = self.launch_game()
                self.GAME_SPEC.increment_time(time.time() - game_time)
                self.clear_map()
                self.app_event = APPEVENT.GAME_STATUS

            elif self.app_event == APPEVENT.GAME_STATUS:
                self.draw_status(self.game_response, self.GAME_SPEC.get_level_to_play())

            # self.clear_map()
            pygame.display.flip()

        pygame.quit()
