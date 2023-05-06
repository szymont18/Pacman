from time import sleep

from MapElements.Vector2d import Vector2d
from gui.Menu.Components.TextArea import TextArea
from gui.TextureFactory import *
from Utility.Engine import *
from MapElements.MapElement import *
from Maps.GameMap import *
from Maps.Level01 import *
from Maps.Level02 import *
from Maps.Level03 import *
from Enums.TileType import *


class App:
    def __init__(self):
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
        self.launch_game()

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

    def draw_win_level(self):
        rectangle = pygame.rect.Rect((100, 200), (514, 400))
        pygame.draw.rect(self.window, "black", rectangle, 0, 5)
        statement = TextArea(Vector2d(200, 100), 514, 100, f'Congratulation !!!', self.window)
        statement2 = TextArea(Vector2d(350, 250), 214, 50, f'Level passed!', self.window, font_size=45, rgb=(247, 245, 245))
        statement3 = TextArea(Vector2d(450, 250), 214, 50, f'Press space to continue', self.window, font_size=45,
                              rgb=(247, 245, 245))

        statement.draw()
        statement2.draw()
        statement3.draw()

    def draw_lose_level(self):
        rectangle = pygame.rect.Rect((100, 200), (514, 400))
        pygame.draw.rect(self.window, "black", rectangle, 0, 5)
        statement = TextArea(Vector2d(200, 100), 514, 100, f'Defeat :(', self.window, rgb=(184, 6, 26))
        statement2 = TextArea(Vector2d(350, 250), 214, 50, f'Level lost!', self.window, font_size=45, rgb=(247, 245, 245))
        statement3 = TextArea(Vector2d(450, 250), 214, 50, f'Press space to continue', self.window, font_size=45,
                              rgb=(247, 245, 245))

        statement.draw()
        statement2.draw()
        statement3.draw()

    def draw_game_win(self):
        rectangle = pygame.rect.Rect((100, 200), (514, 400))
        pygame.draw.rect(self.window, "black", rectangle, 0, 5)
        statement = TextArea(Vector2d(200, 100), 514, 100, f'Congratulations!!!', self.window)
        statement2 = TextArea(Vector2d(350, 250), 214, 50, f'You win the game!', self.window, font_size=45, rgb=(247, 245, 245))
        statement3 = TextArea(Vector2d(450, 250), 214, 50, f'Press space to exit', self.window, font_size=45,
                              rgb=(247, 245, 245))

        statement.draw()
        statement2.draw()
        statement3.draw()

    def launch_game(self):
        pygame.init()
        # #game_map = Level01(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)
        # #engine = Engine(game_map, self.MAX_ROW, self.MAX_COL, self, self.__KEYH, self.FIELD_SIZE)
        #
        response = -10
        game_map = None
        for i in range(1, 4):
            if i == 1:
                game_map = Level01(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)
            elif i == 2:
                game_map = Level02(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)
            elif i == 3:
                game_map = Level03(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)

            engine = Engine(game_map, self.MAX_ROW, self.MAX_COL, self, self.__KEYH, self.FIELD_SIZE)
            response = engine.run()
            print("Odpowiez gry to " + str(response))
            if response != 10:
                break  # If Pacman won 10 value is returned

        if response != 10:
            return

        sleep(0.400)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    self.__KEYH.key_pressed(event)
                elif event.type == pygame.KEYUP:
                    self.__KEYH.key_released(event)

            if self.__KEYH.space_pressed:
                exit(0)

            self.clear_map()
            self.draw_game_win()
            pygame.display.flip()
        # self.window.setScene(gameScene) # In the future
