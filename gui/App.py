import pygame
from gui.TextureFactory import *
from Utility.KeyHandler import *
from Utility.Engine import *
from MapElements.MapElement import *
from Maps.GameMap import *
from Maps.Level01 import *
from Enums.TileType import *

class App:
    def __init__(self):
        self.__TEXTURE_FACTORY = TextureFactory()
        # W przyszłości sparameryzowanie tych wartości w zależności od mapki
        self.MAX_ROW = 17
        self.MAX_COL = 17
        self.FIELD_SIZE = 48

        # Tutaj miejsce na sceny itp

        # Okno
        self.window = pygame.display.set_mode((self.MAX_COL * self.FIELD_SIZE, self.MAX_ROW * self.FIELD_SIZE))



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

        for key in items.keys():
            # print(key.ROW,key.COL)
            item = items.get(key)
            image = self.__TEXTURE_FACTORY.load(item.get_image_path())
            image_adjusted = pygame.transform.scale(image, (self.FIELD_SIZE, self.FIELD_SIZE))
            self.window.blit(image_adjusted, (item.POS_X, item.POS_Y))

    def launch_game(self):
        game_map = Level01(self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE)
        engine = Engine(game_map, self.MAX_ROW, self.MAX_COL, self, self.__KEYH, self.FIELD_SIZE)

        engine.run()
        # self.window.setScene(gameScene) #tu powinno nastapic ustawienie sceny gry zamiast menu
