from time import sleep

import pygame

from gui.Menu.Components.TextArea import TextArea
from gui.TextureFactory import *
from Utility.KeyHandler import *
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
        # W przyszłości sparameryzowanie tych wartości w zależności od mapki
        self.MAX_ROW = 17
        self.MAX_COL = 17
        self.FIELD_SIZE = 42

        # Tutaj miejsce na sceny itp

        # Okno
        self.window = pygame.display.set_mode((self.MAX_COL * self.FIELD_SIZE, (self.MAX_ROW + 2) * self.FIELD_SIZE))

        # Czcionka
        pygame.font.init()
        self.font = pygame.font.SysFont(None, self.FIELD_SIZE)

        # LISTENER
        self.__KEYH = KeyHandler()

        # setMenuScene() metoda renderuje menu
        # setGameScene() metoda renderuje ogolne rozmieszczenie rzeczy podczas gry (mapa,statystyki,przyciski)

        # Normalnie w menu powinien byc guzik wlaczajacy gre ale w dalsze części
        self.launch_game()

    # metoda czysci ekran
    def clear_map(self):
        self.window.fill((0, 0, 0))

    # metoda sluzy do rysowania potworkow i pacmana
    def draw_map_element(self, element: MapElement):
        pos_x = element.get_pos_x()
        pos_y = element.get_pos_y()

        image = self.__TEXTURE_FACTORY.load(element.get_image_path())
        image_adjusted = pygame.transform.scale(image, (self.FIELD_SIZE, self.FIELD_SIZE))
        self.window.blit(image_adjusted, (pos_x, pos_y))

    # metoda do narysowania mapy (mapa jest przechowywana jako obraz)
    def draw_map(self, map: GameMap):
        # image = self.__TEXTURE_FACTORY.load(map.get_image_path())
        # image_adjusted = pygame.transform.scale(image, (self.FIELD_SIZE * self.MAX_ROW, self.FIELD_SIZE * self.MAX_COL))
        # self.window.blit(image_adjusted, (0, 0))

        for row in range(self.MAX_ROW):
            for col in range(self.MAX_COL):
                x, y = col * self.FIELD_SIZE, row * self.FIELD_SIZE
                if map.TILES[row][col].TYPE == TileType.WALL:
                    self.window.blit(map._wall_image, (x, y))
                else:
                    self.window.blit(map._void_image, (x, y))

    def draw_items(self, map: GameMap):
        items: dict() = map.get_items()
        keys_to_removed = []

        for key in items.keys():
            # print(key.ROW,key.COL)
            item = items.get(key)
            #if item.is_active:
            image = self.__TEXTURE_FACTORY.load(item.get_image_path())
            image_adjusted = pygame.transform.scale(image, (self.FIELD_SIZE, self.FIELD_SIZE))
            self.window.blit(image_adjusted, (item.POS_X, item.POS_Y))

            #Zmienilem ze nie App pamieta o sprzataniu tylko silnik w petli update() zeby bylo tak jak z potworkami
            #else:
            #    keys_to_removed.append(key)

        #for key in keys_to_removed:
        #    items.pop(key)

    def draw_pacman_status(self, lives_number: int, score_number: int):
        start_hearth_position = (10, self.MAX_ROW * self.FIELD_SIZE) # 10 to offset ( powinno być sparametryzowane?)
        #print("Draw pacman status", lives_number, score_number)
        for i in range(min(lives_number, 5)): # Maksymalnie 5 życ pokazanych
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
        statement = TextArea((200, 100), 514, 100, f'Congratulation !!!', self.window)
        statement2 = TextArea((350, 250), 214, 50, f'Level passed!', self.window, font_size=45, rgb=(247, 245, 245))
        statement3 = TextArea((450, 250), 214, 50, f'Press space to continue', self.window, font_size=45,
                              rgb=(247, 245, 245))

        statement.draw()
        statement2.draw()
        statement3.draw()

    def draw_lose_level(self):
        rectangle = pygame.rect.Rect((100, 200), (514, 400))
        pygame.draw.rect(self.window, "black", rectangle, 0, 5)
        statement = TextArea((200, 100), 514, 100, f'Defeat :(', self.window, rgb=(184, 6, 26))
        statement2 = TextArea((350, 250), 214, 50, f'Level lost!', self.window, font_size=45, rgb=(247, 245, 245))
        statement3 = TextArea((450, 250), 214, 50, f'Press space to continue', self.window, font_size=45,
                              rgb=(247, 245, 245))

        statement.draw()
        statement2.draw()
        statement3.draw()

    def draw_game_win(self):
        rectangle = pygame.rect.Rect((100, 200), (514, 400))
        pygame.draw.rect(self.window, "black", rectangle, 0, 5)
        statement = TextArea((200, 100), 514, 100, f'Congratulations!!!', self.window)
        statement2 = TextArea((350, 250), 214, 50, f'You win the game!', self.window, font_size=45, rgb=(247, 245, 245))
        statement3 = TextArea((450, 250), 214, 50, f'Press space to exit', self.window, font_size=45,
                              rgb=(247, 245, 245))

        statement.draw()
        statement2.draw()
        statement3.draw()

    def launch_game(self):
        pygame.init()
        # #game_map = Level01(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)
        # #engine = Engine(game_map, self.MAX_ROW, self.MAX_COL, self, self.__KEYH, self.FIELD_SIZE)
        #
        for i in range(1, 4):
            if i==1:
                game_map = Level01(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)
            elif i==2:
                game_map = Level02(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)
            elif i==3:
                game_map = Level03(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)

            engine = Engine(game_map, self.MAX_ROW, self.MAX_COL, self, self.__KEYH, self.FIELD_SIZE)
            response = engine.run()
            print("Odpowiez gry to " + str(response))
            if response !=10: break  #Jesli pacman wygra gre to zwracana jest wartosc 10

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
        # self.window.setScene(gameScene) #tu powinno nastapic ustawienie sceny gry zamiast menu
