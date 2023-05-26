import pygame

from Enums.TileType import TileType
from Maps.Tile import Tile
from ..Components.Image import Image
from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *


class INHAND(Enum):
    DEMON = 1
    GHOST = 2
    SKULL = 3
    PACMAN = 4
    BONUSLIFE = 5
    BONUSMONEY = 6
    REDBALL = 7
    SLOW = 8
    NUKE = 9
    VOID = 10
    WALL = 11
    CROSS = 12


class ICREATOR(Enum):
    MAIN = 0
    COMPONENT = 1
    WALLS = 2
    MONSTER = 3
    BONUSES = 4
    PACMAN = 5


class LevelCreatorScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        self.FIELD_SIZE = 42

        self.tiles_on_screen = 17
        self.rows = 17
        self.cols = 17

        self.offset_row = 0
        self.offset_col = 0

        self.in_hand = None
        self.level_creator_scene = ICREATOR.MAIN

        self.table = [[Tile(TileType.VOID) for i in range(self.cols)] for j in range(self.rows)]

        self.bonus_probabilities = {}

        # For drawning
        self._void_image = pygame.transform.scale(pygame.image.load("resources/tiles/void.png"),
                                                  (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self._wall_image = pygame.transform.scale(pygame.image.load("resources/tiles/wall.png"),
                                                  (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self._cross_image = pygame.transform.scale(pygame.image.load("resources/tiles/cross.png"),
                                                   (self.FIELD_SIZE, self.FIELD_SIZE)).convert()

        # MAIN
        self.save_button = Button(Vector2d(self.rows * self.FIELD_SIZE, 7), 100, self.FIELD_SIZE, "Save",
                                  screen, lambda: self.check_and_save())

        self.add_column = Button(Vector2d(self.rows * self.FIELD_SIZE, 157), 100, self.FIELD_SIZE, "Add Column",
                                 screen, lambda: self.add_new_column())

        self.add_row = Button(Vector2d(self.rows * self.FIELD_SIZE, 307), 100, self.FIELD_SIZE, "Add Row",
                              screen, lambda: self.add_new_row())

        self.add_component = Button(Vector2d(self.rows * self.FIELD_SIZE, 457), 100, self.FIELD_SIZE, "Add Component",
                                    screen, lambda: self.change_creator_scene(ICREATOR.COMPONENT))

        self.return_button = Button(Vector2d(self.rows * self.FIELD_SIZE, 607), 100, self.FIELD_SIZE, "Return",
                                    screen, lambda: Scene.change_menu_scene(SceneTypes.MAIN))

        # COMPONENT
        self.walls = Button(Vector2d(self.rows * self.FIELD_SIZE, 7), 100, self.FIELD_SIZE, "Add wall",
                            screen, lambda: self.change_creator_scene(ICREATOR.WALLS))

        self.monsters = Button(Vector2d(self.rows * self.FIELD_SIZE, 157), 100, self.FIELD_SIZE, "Add monster",
                               screen, lambda: self.change_creator_scene(ICREATOR.MONSTER))

        self.add_bonus = Button(Vector2d(self.rows * self.FIELD_SIZE, 307), 100, self.FIELD_SIZE, "Add Bonus",
                                screen, lambda: self.change_creator_scene(ICREATOR.BONUSES))

        self.pacman_start = Button(Vector2d(self.rows * self.FIELD_SIZE, 457), 100, self.FIELD_SIZE, "Pacman position",
                                   screen, lambda: self.change_creator_scene(ICREATOR.COMPONENT))

        self.return_button_scene = Button(Vector2d(self.rows * self.FIELD_SIZE, 607), 100, self.FIELD_SIZE, "Return",
                                          screen, lambda: self.change_creator_scene(ICREATOR.MAIN))

        # WALLS
        self.void_button = Button(Vector2d(self.rows * self.FIELD_SIZE, 15), self.FIELD_SIZE, self.FIELD_SIZE, "VOID",
                                  screen, lambda: self.change_in_hand(INHAND.VOID))

        self.wall_button = Button(Vector2d(self.rows * self.FIELD_SIZE, 210), self.FIELD_SIZE, self.FIELD_SIZE, "",
                                  screen, lambda: self.change_in_hand(INHAND.WALL))
        self.wall_image = Image(Vector2d(self.rows * self.FIELD_SIZE, 210), self.FIELD_SIZE, self.FIELD_SIZE,
                                screen, "resources/tiles/wall.png")

        self.cross_button = Button(Vector2d(self.rows * self.FIELD_SIZE, 405), self.FIELD_SIZE, self.FIELD_SIZE, "",
                                   screen, lambda: self.change_in_hand(INHAND.CROSS))
        self.cross_image = Image(Vector2d(self.rows * self.FIELD_SIZE, 405), self.FIELD_SIZE, self.FIELD_SIZE,
                                 screen, "resources/tiles/cross.png")

        self.return_to_component = Button(Vector2d(self.rows * self.FIELD_SIZE, 600), 100, self.FIELD_SIZE, "Return",
                                          screen, lambda: self.change_creator_scene(ICREATOR.COMPONENT))

    def draw(self, mouse):
        self.screen.fill((0, 0, 0))

        self.draw_map()
        if self.level_creator_scene == ICREATOR.MAIN:
            self.save_button.draw()
            self.add_column.draw()
            self.add_row.draw()
            self.add_component.draw()
            self.return_button.draw()

            self.save_button.is_clicked(mouse)
            self.add_column.is_clicked(mouse)
            self.add_row.is_clicked(mouse)
            self.add_component.is_clicked(mouse)
            self.return_button.is_clicked(mouse)

        elif self.level_creator_scene == ICREATOR.COMPONENT:
            self.walls.draw()
            self.monsters.draw()
            self.add_bonus.draw()
            self.pacman_start.draw()
            self.return_button.draw()

            self.walls.is_clicked(mouse)
            self.monsters.is_clicked(mouse)
            self.add_bonus.is_clicked(mouse)
            self.pacman_start.is_clicked(mouse)
            self.return_button.is_clicked(mouse)

        elif self.level_creator_scene == ICREATOR.WALLS:
            self.void_button.draw()
            self.wall_image.draw()
            self.cross_image.draw()
            self.return_to_component.draw()

            self.return_to_component.is_clicked(mouse)
            self.void_button.is_clicked(mouse)
            self.wall_button.is_clicked(mouse)
            self.cross_button.is_clicked(mouse)

        if mouse is not None and mouse.type == pygame.MOUSEBUTTONDOWN:
            self.change_tile_status(pygame.mouse.get_pos())

    def draw_map(self):

        for row in range(self.offset_row + self.tiles_on_screen):
            for col in range(self.offset_col + self.tiles_on_screen):
                x, y = (col - self.offset_col) * self.FIELD_SIZE, (row - self.offset_row) * self.FIELD_SIZE
                type = self.table[row][col].TYPE
                if type == TileType.WALL:
                    self.screen.blit(self._wall_image, (x, y))
                elif type == TileType.VOID:
                    self.screen.blit(self._void_image, (x, y))
                elif type == TileType.CROSS:
                    self.screen.blit(self._cross_image, (x, y))

    def change_tile_status(self, mouse_pos):

        if mouse_pos[1] > self.FIELD_SIZE * self.tiles_on_screen: return

        mouse_idx = mouse_pos[0] // self.FIELD_SIZE, mouse_pos[1] // self.FIELD_SIZE
        print(mouse_idx)
        row, col = mouse_idx[1] - self.offset_row, mouse_idx[0] - self.offset_col
        if self.in_hand == INHAND.VOID:
            self.table[row][col] = Tile(TileType.VOID)
        elif self.in_hand == INHAND.WALL:
            self.table[row][col] = Tile(TileType.WALL)
        elif self.in_hand == INHAND.CROSS:
            self.table[row][col] = Tile(TileType.CROSS)

    def change_in_hand(self, new_hand):
        self.in_hand = new_hand

    def check_and_save(self):
        pass

    def add_new_column(self):
        pass

    def add_new_row(self):
        pass

    def change_creator_scene(self, new_scene):
        self.level_creator_scene = new_scene
