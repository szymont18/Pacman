import time
from time import sleep

import pygame.time

from Maps.UserLevel import UserLevel
from gui.Menu.Menu import Menu
from gui.TextureFactory import *
from Utility.Engine import *
from MapElements.MapElement import *
from Maps.GameMap import *
from Maps.Level01 import Level01
from Maps.Level02 import Level02
from Maps.Level03 import Level03
from Maps.Level04 import Level04
from Maps.Level05 import Level05
from Maps.Level06 import Level06
from Maps.Level07 import Level07
from Maps.Level08 import Level08
from Maps.Level09 import Level09
from Maps.Level10 import Level10
from Maps.Level11 import Level11
from Maps.Level12 import Level12
from Maps.Level13 import Level13
from Maps.Level14 import Level14
from Maps.Level15 import Level15
from Maps.Level16 import Level16

from Enums.TileType import *
from enum import Enum
from Enums.RenderType import RenderType


class APPEVENT(Enum):
    MENU = 0
    GAME = 1
    GAME_STATUS = 2


class App:
    def __init__(self):

        # Init pygame
        pygame.init()

        self.FIELD_SIZE = 42
        self.__TEXTURE_FACTORY = TextureFactory(self.FIELD_SIZE)

        # This value will be parameterized in the future. These are max rows and cols that can be shown
        self.MAX_SHOWN_ROWS = 17
        self.MAX_SHOWN_Y = self.MAX_SHOWN_ROWS*self.FIELD_SIZE
        self.MAX_SHOWN_COLS = 17
        self.MAX_SHOWN_X = self.MAX_SHOWN_COLS * self.FIELD_SIZE

        # Window (screen)
        self.window = pygame.display.set_mode((self.MAX_SHOWN_COLS * self.FIELD_SIZE, (self.MAX_SHOWN_ROWS + 2) * self.FIELD_SIZE))
        self.__render_type = None #Has to be assigned in launch game -> It changed the way stuff is drawn on the screen

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

        # For rendering with centered pacman
        self.PACMAN_SCREEN_X = self.MAX_SHOWN_COLS * self.FIELD_SIZE / 2 - self.FIELD_SIZE / 2
        self.PACMAN_SCREEN_Y = self.MAX_SHOWN_ROWS * self.FIELD_SIZE / 2 - self.FIELD_SIZE / 2
        self.__PACMAN = None  # We need to keep track of pacman pos

        # Launch game
        self.app_event = APPEVENT.MENU
        self.game_response = None
        self.launch_app()


    # Clear window
    def clear_map(self):
        self.window.fill((0, 0, 0))

    # Draw pacman and monsters
    def draw_map_element(self, element: MapElement):
        image = self.__TEXTURE_FACTORY.load(element.get_image_path(),self.FIELD_SIZE,self.FIELD_SIZE)
        #image_adjusted = pygame.transform.scale(image, (self.FIELD_SIZE, self.FIELD_SIZE))

        if self.__render_type == RenderType.PACMAN_CENTERED:
            pacman_pos_x = self.__PACMAN.get_pos_x()
            pacman_pos_y = self.__PACMAN.get_pos_y()
            element_pos_x = element.get_pos_x()
            element_pos_y = element.get_pos_y()

            element_screen_x = element_pos_x - pacman_pos_x + self.PACMAN_SCREEN_X
            element_screen_y = element_pos_y - pacman_pos_y + self.PACMAN_SCREEN_Y

            #if(element_screen_x <0 or element_screen_x > self.MAX_SHOWN_X
            #        or element_screen_y < 0 or element_screen_y > self.MAX_SHOWN_Y):
            #    return #Dont draw if it doesnt fit in the screen

            self.window.blit(image, (element_screen_x, element_screen_y))

        else:
            pos_x = element.get_pos_x()
            pos_y = element.get_pos_y()
            self.window.blit(image, (pos_x, pos_y))

    def draw_map(self, game_map: GameMap):
        if game_map.RENDER_TYPE == RenderType.SINGLE_IMAGE:
            map_size_x = self.FIELD_SIZE * game_map.MAX_COL
            map_size_y = self.FIELD_SIZE * game_map.MAX_ROW
            self.window.blit(self.__TEXTURE_FACTORY.load(game_map.get_image_path(), map_size_x, map_size_y), (0, 0))
        else:
            pacman_pos_x = self.__PACMAN.get_pos_x()
            pacman_pos_y = self.__PACMAN.get_pos_y()

            for row in range(game_map.MAX_ROW):
                for col in range(game_map.MAX_COL):
                    tile_pos_x, tile_pos_y = col * self.FIELD_SIZE, row * self.FIELD_SIZE

                    tile_screen_x = tile_pos_x
                    tile_screen_y = tile_pos_y

                    if self.__render_type == RenderType.PACMAN_CENTERED:
                        tile_screen_x = tile_pos_x - pacman_pos_x + self.PACMAN_SCREEN_X
                        tile_screen_y = tile_pos_y - pacman_pos_y + self.PACMAN_SCREEN_Y

                    tile = game_map.TILES[row][col]

                    self.window.blit(self.__TEXTURE_FACTORY.load(tile.get_image_path(),self.FIELD_SIZE,self.FIELD_SIZE),
                                     (tile_screen_x, tile_screen_y))


    def draw_items(self, game_map: GameMap):
        pacman_pos_x = self.__PACMAN.get_pos_x()
        pacman_pos_y = self.__PACMAN.get_pos_y()

        items = game_map.get_items()

        for key in items.keys():
            item = items.get(key)

            item_screen_x = item.POS_X
            item_screen_y = item.POS_Y

            if self.__render_type == RenderType.PACMAN_CENTERED:
                item_screen_x = item.POS_X - pacman_pos_x + self.PACMAN_SCREEN_X
                item_screen_y = item.POS_Y - pacman_pos_y + self.PACMAN_SCREEN_Y

            image = self.__TEXTURE_FACTORY.load(item.get_image_path(),self.FIELD_SIZE,self.FIELD_SIZE)

            self.window.blit(image, (item_screen_x,item_screen_y))

    def draw_portals(self,game_map):
        pacman_pos_x = self.__PACMAN.get_pos_x()
        pacman_pos_y = self.__PACMAN.get_pos_y()

        for portal_row,portal_col in game_map.PORTALS:
            portal_pos_x = portal_col*self.FIELD_SIZE
            portal_pos_y = portal_row * self.FIELD_SIZE

            portal_screen_x = portal_pos_x
            portal_screen_y = portal_pos_y

            if self.__render_type == RenderType.PACMAN_CENTERED:
                portal_screen_x = portal_pos_x - pacman_pos_x + self.PACMAN_SCREEN_X
                portal_screen_y = portal_pos_y - pacman_pos_y + self.PACMAN_SCREEN_Y

            self.window.blit(self.__TEXTURE_FACTORY.load("resources/tiles/portal.png",self.FIELD_SIZE,self.FIELD_SIZE),
                                 (portal_screen_x, portal_screen_y))

    def draw_pacman_status(self, lives_number: int, score_number: int):
        start_hearth_position = (10, self.MAX_SHOWN_ROWS * self.FIELD_SIZE)  # OFFSET (should be parametrized ?) (???)

        for i in range(min(lives_number, 5)):  # MAX 5 lives can be showed
            self.window.blit(self.__TEXTURE_FACTORY.load("resources/items/BonusLife1.png",self.FIELD_SIZE,self.FIELD_SIZE), start_hearth_position)
            start_hearth_position = (start_hearth_position[0] + self.FIELD_SIZE, start_hearth_position[1])

        if lives_number > 5:
            img = self.font.render("...", True, "white")
            self.window.blit(img, start_hearth_position)

        score_img = self.font.render("SCORE: " + str(score_number), True, "white")
        self.window.blit(score_img, (self.MAX_SHOWN_COLS * (self.FIELD_SIZE - 15), self.MAX_SHOWN_ROWS * self.FIELD_SIZE))


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
                self.event = event

            self.menu.draw(self.event)

    def launch_game(self):
        self.clear_map()
        game_map = None
        if self.GAME_SPEC.pathname is not None:
            print("Chosed game_map")
            game_map = UserLevel(self.FIELD_SIZE,self.GAME_SPEC.pathname)
            self.__render_type = game_map.RENDER_TYPE

        else:
            level_id = self.GAME_SPEC.get_level_to_play()
            #hardness = self.GAME_SPEC.get_hardness()  # Should do sth to change hardness of the game (number of enemies)            # TODO After map parsing

            levels = [Level01,Level02,Level03,Level04,Level05,Level06,
                      Level07,Level08,Level09,Level10,Level11,Level12,
                      Level13,Level14,Level15,Level16]
            actual_level = levels[level_id]
            game_map = actual_level(self.FIELD_SIZE)
            self.__render_type = game_map.RENDER_TYPE

        engine = Engine(game_map, game_map.MAX_ROW, game_map.MAX_COL, self, self.__KEYH, self.FIELD_SIZE,
                            self.GAME_SPEC)
        return engine.run()

    def draw_status(self, game_response, level_id):

        self.clear_map()
        if game_response is not None:
            self.GAME_SPEC.set_start_game(False)

        if game_response == STATUS.LVL_WIN and level_id == 2:  # For presentation change to 2
            self.level_status_scene.change_game_status(STATUS.GAME_WIN)

        elif game_response == STATUS.LVL_WIN and level_id < 15:
            self.level_status_scene.change_game_status(STATUS.LVL_WIN)

        elif game_response == STATUS.LVL_LOSE:
            self.level_status_scene.change_game_status(STATUS.LVL_LOSE)

        self.level_status_scene.draw(None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.KEEP_RUNNING = False

            self.level_status_scene.draw(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                print("jestem tutaj")
                if self.GAME_SPEC.pathname is not None:
                    self.GAME_SPEC.pathname = None
                    self.app_event = APPEVENT.MENU
                    break

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

    def assign_pacman(self,pacman):
        self.__PACMAN = pacman