import pygame

from Enums.MonsterTypes import MonsterTypes
from Enums.TileType import TileType
from Items.BonusLife import BonusLife
from Items.BonusMoney import BonusMoney
from Items.Nuke import Nuke
from Items.Slow import Slow
from Maps.Tile import Tile
from ..Components.Image import Image
from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *
from ..Components.TextInput import TextInput


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
    DELETE_ROW = 13
    DELETE_COL = 14
    LAVA = 15
    DOT = 16
    EGG = 17


class ICREATOR(Enum):
    MAIN = 0
    COMPONENT = 1
    WALLS = 2
    MONSTER = 3
    BONUSES = 4
    PACMAN = 5
    SIZE = 6
    SAVE = 7
    DIALOG = 8
    INTRODUCTION = 9


class LevelCreatorScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        self.FIELD_SIZE = 42
        self.START_ROWS = 17
        self.MENU_ROW_COORD = self.START_ROWS * self.FIELD_SIZE + 10

        self.rows = 17
        self.cols = 17

        self.offset_row = 0
        self.offset_col = 0

        self.in_hand = None
        self.level_creator_scene = ICREATOR.INTRODUCTION

        # self.table = [[Tile(TileType.VOID) for i in range(self.cols)] for j in range(self.rows)]
        self.table = {(row, col): Tile(TileType.VOID) for col in range(self.cols) for row in range(self.rows)}
        self.bonus_probabilities = {}
        self.on_load_monsters = {}
        self.monster_spawn_tiles = {}
        self.dots = {}
        self.red_dots = {}
        self.pacman_x = None
        self.pacman_y = None

        # For drawning
        self.__void_image = pygame.transform.scale(pygame.image.load("resources/tiles/void.png"),
                                                   (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__wall_image = pygame.transform.scale(pygame.image.load("resources/tiles/wall.png"),
                                                   (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__cross_image = pygame.transform.scale(pygame.image.load("resources/tiles/cross.png"),
                                                    (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__lava_image = pygame.transform.scale(pygame.image.load("resources/tiles/LAVA.png"),
                                                   (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__dot_image = pygame.transform.scale(pygame.image.load("resources/items/Dot.png"),
                                                  (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__money_image = pygame.transform.scale(pygame.image.load("resources/items/BonusMoney1.png"),
                                                    (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__red_ball_image = pygame.transform.scale(pygame.image.load("resources/items/RedBall1.png"),
                                                       (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__nuke_image = pygame.transform.scale(pygame.image.load("resources/items/Nuke1.png"),
                                                   (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__slow_image = pygame.transform.scale(pygame.image.load("resources/items/SLOW_1.png"),
                                                   (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__live_image = pygame.transform.scale(pygame.image.load("resources/items/BonusLife1.png"),
                                                   (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__demon_image = pygame.transform.scale(pygame.image.load("resources/demon/D_LEFT_1.png"),
                                                    (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__skull_image = pygame.transform.scale(pygame.image.load("resources/skull/S_LEFT_1.png"),
                                                    (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__ghost_image = pygame.transform.scale(pygame.image.load("resources/ghost/G_LEFT_1.png"),
                                                    (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__egg_image = pygame.transform.scale(pygame.image.load("resources/ghost/G_EGG_1.png"),
                                                  (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        self.__pacman_image = pygame.transform.scale(pygame.image.load("resources/pacman/P_left_1.png"),
                                                     (self.FIELD_SIZE, self.FIELD_SIZE)).convert()
        # Common
        self.__up_array_image = Image(Vector2d(self.START_ROWS * self.FIELD_SIZE, 628),
                                      20, 20, self.screen, "resources/menu/up.png")
        self.__down_array_image = Image(Vector2d((self.START_ROWS + 1) * self.FIELD_SIZE, 628),
                                        20, 20, self.screen, "resources/menu/down.png")
        self.__left_array_image = Image(Vector2d(self.START_ROWS * self.FIELD_SIZE + 21, 592),
                                        20, 20, self.screen, "resources/menu/left.png")
        self.__right_array_image = Image(Vector2d(self.START_ROWS * self.FIELD_SIZE + 21, 664),
                                         20, 20, self.screen, "resources/menu/right.png")

        self.__up_array_image_button = Button(Vector2d(self.START_ROWS * self.FIELD_SIZE, 628),
                                              20, 20, "", self.screen, lambda: self.change_drawing_boundaries((-1, 0)))
        self.__down_array_image_button = Button(Vector2d((self.START_ROWS + 1) * self.FIELD_SIZE, 628),
                                                20, 20, "", self.screen, lambda: self.change_drawing_boundaries((1, 0)))
        self.__left_array_image_button = Button(Vector2d(self.START_ROWS * self.FIELD_SIZE + 21, 592),
                                                20, 20, "", self.screen,
                                                lambda: self.change_drawing_boundaries((0, -1)))
        self.__right_array_image_button = Button(Vector2d(self.START_ROWS * self.FIELD_SIZE + 21, 664),
                                                 20, 20, "", self.screen,
                                                 lambda: self.change_drawing_boundaries((0, 1)))

        # MAIN
        self.change_size = Button(Vector2d(self.MENU_ROW_COORD, 2), 110, self.FIELD_SIZE, "Change size",
                                  screen, lambda: self.change_creator_scene(ICREATOR.SIZE), font_size=25)

        self.add_component = Button(Vector2d(self.MENU_ROW_COORD, 152), 110, self.FIELD_SIZE, "Components",
                                    screen, lambda: self.change_creator_scene(ICREATOR.COMPONENT), font_size=25)

        self.save = Button(Vector2d(self.MENU_ROW_COORD, 302), 110, self.FIELD_SIZE, "Save",
                           screen, lambda: self.check_and_save(), font_size=25)

        self.return_button = Button(Vector2d(self.MENU_ROW_COORD, 452), 110, self.FIELD_SIZE, "Return",
                                    screen, lambda: self.return_to_menu_routine(), font_size=25)

        # SIZE
        self.add_row = Button(Vector2d(self.MENU_ROW_COORD, 10), 100, self.FIELD_SIZE, "Add row",
                              screen, lambda: self.add_new_row(), font_size=25)

        self.add_col = Button(Vector2d(self.MENU_ROW_COORD, 262), 100, self.FIELD_SIZE, "Add column",
                              screen, lambda: self.add_new_column(), font_size=25)

        self.return_button_size = Button(Vector2d(self.MENU_ROW_COORD, 472), 100, self.FIELD_SIZE, "Return",
                                         screen, lambda: self.change_creator_scene(ICREATOR.MAIN), font_size=25)

        # COMPONENT
        self.walls = Button(Vector2d(self.MENU_ROW_COORD, 12), 100, self.FIELD_SIZE, "Walls",
                            screen, lambda: self.change_creator_scene(ICREATOR.WALLS), font_size=25)

        self.monsters = Button(Vector2d(self.MENU_ROW_COORD, 127), 100, self.FIELD_SIZE, "Monsters",
                               screen, lambda: self.change_creator_scene(ICREATOR.MONSTER), font_size=25)

        self.add_bonus = Button(Vector2d(self.MENU_ROW_COORD, 242), 100, self.FIELD_SIZE, "Bonuses",
                                screen, lambda: self.change_creator_scene(ICREATOR.BONUSES), font_size=25)

        self.pacman_start = Button(Vector2d(self.MENU_ROW_COORD, 357), 100, self.FIELD_SIZE, "Pacman",
                                   screen, lambda: self.change_creator_scene(ICREATOR.PACMAN), font_size=25)

        self.return_button_scene = Button(Vector2d(self.MENU_ROW_COORD, 472), 100, self.FIELD_SIZE, "Return",
                                          screen, lambda: self.change_creator_scene(ICREATOR.MAIN), font_size=25)

        # WALLS
        self.void_button = Button(Vector2d(self.MENU_ROW_COORD, 12), self.FIELD_SIZE, self.FIELD_SIZE, "VOID",
                                  screen, lambda: self.change_in_hand(INHAND.VOID))

        self.wall_button = Button(Vector2d(self.MENU_ROW_COORD, 127), self.FIELD_SIZE, self.FIELD_SIZE, "",
                                  screen, lambda: self.change_in_hand(INHAND.WALL))
        self.wall_image = Image(Vector2d(self.MENU_ROW_COORD, 127), self.FIELD_SIZE, self.FIELD_SIZE,
                                screen, "resources/tiles/wall.png")

        self.cross_button = Button(Vector2d(self.MENU_ROW_COORD, 242), self.FIELD_SIZE, self.FIELD_SIZE, "",
                                   screen, lambda: self.change_in_hand(INHAND.CROSS))
        self.cross_image = Image(Vector2d(self.MENU_ROW_COORD, 242), self.FIELD_SIZE, self.FIELD_SIZE,
                                 screen, "resources/tiles/cross.png")

        self.lava_button = Button(Vector2d(self.MENU_ROW_COORD, 357), self.FIELD_SIZE, self.FIELD_SIZE, "",
                                  screen, lambda: self.change_in_hand(INHAND.LAVA))
        self.lava_image = Image(Vector2d(self.MENU_ROW_COORD, 357), self.FIELD_SIZE, self.FIELD_SIZE,
                                screen, "resources/tiles/LAVA.png")

        self.return_to_component = Button(Vector2d(self.MENU_ROW_COORD, 472), 100, self.FIELD_SIZE, "Return",
                                          screen, lambda: self.change_creator_scene(ICREATOR.COMPONENT), font_size=25)

        # Monsters
        self.skull = Button(Vector2d(self.MENU_ROW_COORD, 12), self.FIELD_SIZE, self.FIELD_SIZE, "",
                            screen, lambda: self.change_in_hand(INHAND.SKULL), font_size=25)
        self.skull_image = Image(Vector2d(self.MENU_ROW_COORD, 12), self.FIELD_SIZE, self.FIELD_SIZE,
                                 screen, "resources/skull/S_LEFT_1.png")

        self.demon = Button(Vector2d(self.MENU_ROW_COORD, 127), self.FIELD_SIZE, self.FIELD_SIZE, "",
                            screen, lambda: self.change_in_hand(INHAND.DEMON), font_size=25)
        self.demon_image = Image(Vector2d(self.MENU_ROW_COORD, 127), self.FIELD_SIZE, self.FIELD_SIZE,
                                 screen, "resources/demon/D_LEFT_1.png")

        self.ghost = Button(Vector2d(self.MENU_ROW_COORD, 242), self.FIELD_SIZE, self.FIELD_SIZE, "",
                            screen, lambda: self.change_in_hand(INHAND.GHOST), font_size=25)
        self.ghost_image = Image(Vector2d(self.MENU_ROW_COORD, 242), self.FIELD_SIZE, self.FIELD_SIZE,
                                 screen, "resources/ghost/G_LEFT_1.png")
        self.egg = Button(Vector2d(self.MENU_ROW_COORD, 357), self.FIELD_SIZE, self.FIELD_SIZE, "",
                          screen, lambda: self.change_in_hand(INHAND.EGG), font_size=25)
        self.egg_image = Image(Vector2d(self.MENU_ROW_COORD, 357), self.FIELD_SIZE, self.FIELD_SIZE,
                               screen, "resources/ghost/G_EGG_1.png")

        self.return_button_monsters = Button(Vector2d(self.MENU_ROW_COORD, 452), 110, self.FIELD_SIZE, "Return",
                                             screen, lambda: self.change_creator_scene(ICREATOR.COMPONENT),
                                             font_size=25)

        # Bonuses
        self.dot = Button(Vector2d(self.MENU_ROW_COORD, 6), self.FIELD_SIZE, self.FIELD_SIZE, "",
                          screen, lambda: self.change_in_hand(INHAND.DOT), font_size=25)
        self.dot_image = Image(Vector2d(self.MENU_ROW_COORD, 6), self.FIELD_SIZE, self.FIELD_SIZE,
                               screen, "resources/items/Dot.png")
        self.dot_button = Button(Vector2d(self.MENU_ROW_COORD + self.FIELD_SIZE, 6), self.FIELD_SIZE, 20,
                                 "FILL ALL", self.screen, lambda: self.load_white_dots(), font_size=20)

        self.red_ball = Button(Vector2d(self.MENU_ROW_COORD, 82), self.FIELD_SIZE, self.FIELD_SIZE, "",
                               screen, lambda: self.change_in_hand(INHAND.REDBALL), font_size=25)
        self.red_ball_image = Image(Vector2d(self.MENU_ROW_COORD, 82), self.FIELD_SIZE, self.FIELD_SIZE,
                                    screen, "resources/items/RedBall1.png")

        self.live = Button(Vector2d(self.MENU_ROW_COORD, 158), self.FIELD_SIZE, self.FIELD_SIZE, "",
                           screen, lambda: self.change_in_hand(INHAND.BONUSLIFE), font_size=25)
        self.live_image = Image(Vector2d(self.MENU_ROW_COORD, 158), self.FIELD_SIZE, self.FIELD_SIZE,
                                screen, "resources/items/BonusLife1.png")
        self.live_input = TextInput(Vector2d(self.MENU_ROW_COORD + self.FIELD_SIZE, 158), self.FIELD_SIZE // 2, 20,
                                    self.screen, font_size=20)
        self.live_add_button = Button(Vector2d(self.MENU_ROW_COORD + self.FIELD_SIZE, 180), self.FIELD_SIZE // 2,
                                      20, "+", screen, lambda: self.add_bonus_prob(BonusLife.__name__, self.live_input.text),
                                      font_size=15)

        self.money = Button(Vector2d(self.MENU_ROW_COORD, 234), self.FIELD_SIZE, self.FIELD_SIZE, "",
                            screen, lambda: self.change_in_hand(INHAND.BONUSMONEY), font_size=25)
        self.money_image = Image(Vector2d(self.MENU_ROW_COORD, 234), self.FIELD_SIZE, self.FIELD_SIZE,
                                 screen, "resources/items/BonusMoney1.png")
        self.money_input = TextInput(Vector2d(self.MENU_ROW_COORD + self.FIELD_SIZE, 234), self.FIELD_SIZE // 2, 20,
                                     self.screen, font_size=20)
        self.money_add_button = Button(Vector2d(self.MENU_ROW_COORD + self.FIELD_SIZE, 256), self.FIELD_SIZE // 2,
                                      20, "+", screen, lambda: self.add_bonus_prob(BonusMoney.__name__, self.money_input.text),
                                      font_size=15)

        self.slow = Button(Vector2d(self.MENU_ROW_COORD, 310), self.FIELD_SIZE, self.FIELD_SIZE, "",
                           screen, lambda: self.change_in_hand(INHAND.SLOW), font_size=25)
        self.slow_image = Image(Vector2d(self.MENU_ROW_COORD, 310), self.FIELD_SIZE, self.FIELD_SIZE,
                                screen, "resources/items/SLOW_1.png")
        self.slow_input = TextInput(Vector2d(self.MENU_ROW_COORD + self.FIELD_SIZE, 310), self.FIELD_SIZE // 2, 20,
                                    self.screen, font_size=20)
        self.slow_add_button = Button(Vector2d(self.MENU_ROW_COORD + self.FIELD_SIZE, 332), self.FIELD_SIZE // 2,
                                      20, "+", screen, lambda: self.add_bonus_prob(Slow.__name__, self.slow_input.text),font_size=15)

        self.nuke = Button(Vector2d(self.MENU_ROW_COORD, 386), self.FIELD_SIZE, self.FIELD_SIZE, "",
                           screen, lambda: self.change_in_hand(INHAND.NUKE), font_size=25)
        self.nuke_image = Image(Vector2d(self.MENU_ROW_COORD, 386), self.FIELD_SIZE, self.FIELD_SIZE,
                                screen, "resources/items/NUKE1.png")
        self.nuke_input = TextInput(Vector2d(self.MENU_ROW_COORD + self.FIELD_SIZE, 386), self.FIELD_SIZE//2, 20,
                                    self.screen, font_size=20)
        self.nuke_add_button = Button(Vector2d(self.MENU_ROW_COORD + self.FIELD_SIZE, 408), self.FIELD_SIZE // 2,
                                      20, "+", screen, lambda: self.add_bonus_prob(Nuke.__name__, self.nuke_input.text),
                                      font_size=15)

        self.return_button_bonuses = Button(Vector2d(self.MENU_ROW_COORD, 452), 110, self.FIELD_SIZE, "Return",
                                            screen, lambda: self.change_creator_scene(ICREATOR.COMPONENT),
                                            font_size=25)

        self.test_input = TextInput(Vector2d(0, 0), 200, 200, self.screen,
                                    font_size=10)
        # Pacman
        self.pacman = Button(Vector2d(self.MENU_ROW_COORD, 205), self.FIELD_SIZE, self.FIELD_SIZE, "",
                             screen, lambda: self.change_in_hand(INHAND.PACMAN), font_size=25)
        self.pacman_image = Image(Vector2d(self.MENU_ROW_COORD, 205), self.FIELD_SIZE, self.FIELD_SIZE,
                                  screen, "resources/pacman/P_left_1.png")

        # Save
        self.save_map_announcement = TextArea(Vector2d(450, 250), 214, 50,
                                              f'Enter the name of the map and press the save button', self.screen,
                                              font_size=32, rgb=(247, 245, 245))

        self.map_name = TextInput(Vector2d(600, 250), 214, 50, screen, font_size=50)
        self.confirm_button = Button(Vector2d(660, 250), 214, 50, "Save", screen, lambda: self.save_to_file())

        # Dialog
        self.dialog_text = TextArea(Vector2d(450, 250), 214, 50,f'empty', self.screen, font_size=32, rgb=(247, 245, 245))
        self.dialog_return = Button(Vector2d(660, 250), 214, 50, "Return", screen,
                                    lambda: self.change_creator_scene(ICREATOR.MAIN))

        # Introduction
        self.introduction_plain_text = "Map Creator is a tool that allows you to create your own map. To create a " \
                                       "map, you will need to: place a PACMAN, place at least ONE EGG and ONE  " \
                                       "MONSTER, place at least ONE BONUS. To place an item on the map, simply go to " \
                                       "the appropriate section, click on the desired icon, and then click on the " \
                                       "location on the map where you want to place the item.\n NOTE! An exception " \
                                       "applies to items for which we only select the frequency of occurrence, " \
                                       "and their placement is chosen randomly by the game. To remove an item from " \
                                       "the map, right-click on it.\n Have fun!"

        self.introduction_text = TextArea(Vector2d(10, 100), 514, 500,self.introduction_plain_text, self.screen, font_size=32,
                                          rgb=(247, 245, 245))
        self.create_button = Button(Vector2d(650, 250), 214, 50, "Let's create", screen,
                                    lambda: self.change_creator_scene(ICREATOR.MAIN))

    def init_map(self):
        self.rows = 17
        self.cols = 17

        self.offset_row = 0
        self.offset_col = 0

        self.in_hand = None
        self.level_creator_scene = ICREATOR.MAIN
        self.table = {(row, col): Tile(TileType.VOID) for col in range(self.cols) for row in range(self.rows)}
        self.bonus_probabilities = {}
        self.on_load_monsters = {}
        self.monster_spawn_tiles = {}
        self.dots = {}
        self.red_dots = {}
        self.pacman_x = None
        self.pacman_y = None

    def draw(self, mouse):
        self.screen.fill((0, 0, 0))

        self.draw_map()
        self.draw_monsters()
        self.draw_items()
        self.draw_pacman()
        self.__up_array_image.draw()
        self.__down_array_image.draw()
        self.__left_array_image.draw()
        self.__right_array_image.draw()

        self.__down_array_image_button.is_clicked(mouse)
        self.__up_array_image_button.is_clicked(mouse)
        self.__left_array_image_button.is_clicked(mouse)
        self.__right_array_image_button.is_clicked(mouse)

        if self.level_creator_scene == ICREATOR.MAIN:
            self.change_size.draw()
            self.add_component.draw()
            self.save.draw()
            self.add_component.draw()
            self.return_button.draw()

            self.change_size.is_clicked(mouse)
            self.add_component.is_clicked(mouse)
            self.save.is_clicked(mouse)
            self.add_component.is_clicked(mouse)
            self.return_button.is_clicked(mouse)

        elif self.level_creator_scene == ICREATOR.SIZE:
            self.add_col.draw()
            self.add_row.draw()
            self.return_button_size.draw()

            self.return_button_size.is_clicked(mouse)
            self.add_col.is_clicked(mouse)
            self.add_row.is_clicked(mouse)

        elif self.level_creator_scene == ICREATOR.COMPONENT:
            self.walls.draw()
            self.monsters.draw()
            self.add_bonus.draw()
            self.pacman_start.draw()
            self.return_button_scene.draw()

            self.walls.is_clicked(mouse)
            self.monsters.is_clicked(mouse)
            self.add_bonus.is_clicked(mouse)
            self.pacman_start.is_clicked(mouse)
            self.return_button_scene.is_clicked(mouse)

        # Walls
        elif self.level_creator_scene == ICREATOR.WALLS:
            self.void_button.draw()
            self.wall_image.draw()
            self.cross_image.draw()
            self.lava_image.draw()
            self.return_to_component.draw()

            self.lava_button.is_clicked(mouse)
            self.return_to_component.is_clicked(mouse)
            self.void_button.is_clicked(mouse)
            self.wall_button.is_clicked(mouse)
            self.cross_button.is_clicked(mouse)

        # Monsters
        elif self.level_creator_scene == ICREATOR.MONSTER:
            self.skull_image.draw()
            self.demon_image.draw()
            self.ghost_image.draw()
            self.egg_image.draw()
            self.return_button_monsters.draw()

            self.egg.is_clicked(mouse)
            self.skull.is_clicked(mouse)
            self.demon.is_clicked(mouse)
            self.ghost.is_clicked(mouse)
            self.return_button_monsters.is_clicked(mouse)

        # Bonuses
        elif self.level_creator_scene == ICREATOR.BONUSES:
            self.dot_image.draw()
            self.red_ball_image.draw()
            self.live_image.draw()
            self.slow_image.draw()
            self.money_image.draw()
            self.nuke_image.draw()
            self.return_button_monsters.draw()
            self.dot_button.draw()
            self.nuke_input.update()
            self.nuke_input.draw()
            self.slow_input.update()
            self.slow_input.draw()
            self.slow_add_button.draw()
            self.slow_add_button.is_clicked(mouse)
            self.nuke_add_button.draw()
            self.nuke_add_button.is_clicked(mouse)
            self.live_add_button.draw()
            self.live_add_button.is_clicked(mouse)
            self.money_add_button.draw()
            self.money_add_button.is_clicked(mouse)
            self.live_input.update()
            self.live_input.draw()
            self.money_input.update()
            self.money_input.draw()

            if mouse is not None and mouse.type == pygame.KEYDOWN and mouse.key == pygame.K_SPACE: return
            self.dot_button.is_clicked(mouse)
            self.money_input.is_clicked(mouse)
            self.live_input.is_clicked(mouse)
            self.slow_input.is_clicked(mouse)
            self.nuke_input.is_clicked(mouse)
            self.dot.is_clicked(mouse)
            self.live.is_clicked(mouse)
            self.red_ball.is_clicked(mouse)
            self.money.is_clicked(mouse)
            self.slow.is_clicked(mouse)
            self.nuke.is_clicked(mouse)
            self.return_button_monsters.is_clicked(mouse)

        elif self.level_creator_scene == ICREATOR.PACMAN:
            self.pacman_image.draw()
            self.return_button_monsters.draw()

            self.return_button_monsters.is_clicked(mouse)
            self.pacman.is_clicked(mouse)

        elif self.level_creator_scene == ICREATOR.SAVE:
            if mouse is not None and mouse.type == pygame.KEYDOWN and mouse.key == pygame.K_SPACE: return

            self.screen.fill((0, 0, 0))
            self.map_name.is_clicked(mouse)
            self.map_name.update()
            self.map_name.draw()
            self.save_map_announcement.draw()
            self.confirm_button.draw()
            self.confirm_button.is_clicked(mouse)

        elif self.level_creator_scene == ICREATOR.DIALOG:
            self.screen.fill((0, 0, 0))
            self.dialog_text.draw()
            self.dialog_return.draw()
            self.dialog_return.is_clicked(mouse)

        elif self.level_creator_scene == ICREATOR.INTRODUCTION:
            self.introduction_text.draw()
            self.create_button.draw()
            self.create_button.is_clicked(mouse)

        if mouse is not None and mouse.type == pygame.MOUSEBUTTONDOWN and mouse.button == 3: # Right mouse click
            self.delete_obstacles(pygame.mouse.get_pos())

        elif mouse is not None and mouse.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(pygame.mouse.get_pos())

    def draw_map(self):

        for row in range(self.offset_row + self.START_ROWS):
            for col in range(self.offset_col + self.START_ROWS):
                x, y = (col - self.offset_col) * self.FIELD_SIZE, (row - self.offset_row) * self.FIELD_SIZE
                type = self.table[(row, col)].TYPE
                if type == TileType.WALL:
                    self.screen.blit(self.__wall_image, (x, y))
                elif type == TileType.VOID:
                    self.screen.blit(self.__void_image, (x, y))
                elif type == TileType.CROSS:
                    self.screen.blit(self.__cross_image, (x, y))
                elif type == TileType.LAVA:
                    self.screen.blit(self.__lava_image, (x, y))

    def is_occupied(self, row, col):
        if row >= self.rows or col >= self.cols: return False
        occupied = False
        if self.table.get((row, col)).TYPE != TileType.VOID:
            occupied = True
        elif self.red_dots.get((row, col)) is not None:
            occupied = True # (???)
        elif self.dots.get((row, col)) is not None:
            occupied = True
        elif self.on_load_monsters.get((row, col)) is not None:
            occupied = True
        elif self.monster_spawn_tiles.get((row, col)) is not None:
            occupied = True
        print(occupied)
        return occupied

    def handle_click(self, mouse_pos):
        if mouse_pos[1] > self.FIELD_SIZE * self.START_ROWS: return
        mouse_idx = mouse_pos[0] // self.FIELD_SIZE, mouse_pos[1] // self.FIELD_SIZE
        row, col = mouse_idx[1] + self.offset_row, mouse_idx[0] + self.offset_col
        print(f'Row = {row}; col = {col}; inhand = {self.in_hand}')

        if self.is_occupied(row, col): return

        if self.in_hand == INHAND.VOID:
            self.table[(row, col)] = Tile(TileType.VOID)

        elif self.in_hand == INHAND.WALL:
            self.table[(row, col)] = Tile(TileType.WALL)
        elif self.in_hand == INHAND.CROSS:
            self.table[(row, col)] = Tile(TileType.CROSS)
        elif self.in_hand == INHAND.LAVA:
            self.table[(row, col)] = Tile(TileType.LAVA)
        elif self.in_hand == INHAND.GHOST:
            self.on_load_monsters[(row, col)] = MonsterTypes.GHOST
        elif self.in_hand == INHAND.DEMON:
            self.on_load_monsters[(row, col)] = MonsterTypes.DEMON
        elif self.in_hand == INHAND.SKULL:
            self.on_load_monsters[(row, col)] = MonsterTypes.SKULL
        elif self.in_hand == INHAND.EGG:
            self.monster_spawn_tiles[(row, col)] = True
        elif self.in_hand == INHAND.DOT:
            self.dots[(row, col)] = True
        elif self.in_hand == INHAND.REDBALL:
            self.red_dots[(row, col)] = True
        # elif self.in_hand == INHAND.SLOW:
        #     self.add_bonus_prob(Slow.__name__, row, col, self.slow_input.text)
        # elif self.in_hand == INHAND.BONUSLIFE:
        #     self.add_bonus_prob(BonusLife.__name__, row, col, self.live_input.text)
        # elif self.in_hand == INHAND.NUKE:
        #     self.add_bonus_prob(Nuke.__name__, row, col, self.nuke_input.text)
        # elif self.in_hand == INHAND.BONUSMONEY:
        #     self.add_bonus_prob(BonusMoney.__name__, row, col, self.money_input.text)
        # elif self.in_hand == INHAND.DELETE_ROW:
        #     self.delete_new_row(row)
        # elif self.in_hand == INHAND.DELETE_COL:
        #     self.delete_new_col(col)
        elif self.in_hand == INHAND.PACMAN:
            self.pacman_x = col
            self.pacman_y = row

    def delete_obstacles(self, mouse_pos):
        print("delete sth")
        if mouse_pos[1] > self.FIELD_SIZE * self.START_ROWS: return
        mouse_idx = mouse_pos[0] // self.FIELD_SIZE, mouse_pos[1] // self.FIELD_SIZE
        row, col = mouse_idx[1] + self.offset_row, mouse_idx[0] + self.offset_col

        if self.table.get((row, col)).TYPE != TileType.VOID:
            self.table.pop((row, col), None)
            self.table[(row, col)] = Tile(TileType.VOID)

        self.red_dots.pop((row, col), None)
        self.dots.pop((row, col), None)
        self.on_load_monsters.pop((row, col), None)
        self.monster_spawn_tiles.pop((row, col), None)

    def draw_pacman(self):
        if self.pacman_x is not None and self.pacman_y is not None:
            row, col = self.pacman_y, self.pacman_x
            if not (self.offset_row <= row < self.offset_row + self.START_ROWS): return
            if not (self.offset_col <= col < self.offset_col + self.START_ROWS): return

            x, y = (col - self.offset_col) * self.FIELD_SIZE, (row - self.offset_row) * self.FIELD_SIZE
            self.screen.blit(self.__pacman_image, (x, y))

    def draw_items(self):
        for pos, flag in self.dots.items():
            if not flag: continue
            row, col = pos
            if not (self.offset_row <= row < self.offset_row + self.START_ROWS): continue
            if not (self.offset_col <= col < self.offset_col + self.START_ROWS): continue

            x, y = (col - self.offset_col) * self.FIELD_SIZE, (row - self.offset_row) * self.FIELD_SIZE
            self.screen.blit(self.__dot_image, (x, y))

        for pos, flag in self.red_dots.items():
            if not flag: continue
            row, col = pos
            if not (self.offset_row <= row < self.offset_row + self.START_ROWS): continue
            if not (self.offset_col <= col < self.offset_col + self.START_ROWS): continue
            x, y = (col - self.offset_col) * self.FIELD_SIZE, (row - self.offset_row) * self.FIELD_SIZE
            self.screen.blit(self.__red_ball_image, (x, y))

        # To uncomment
        # for bonus_type, spec in self.bonus_probabilities.items():
        #     _, (row, col) = spec
        #     if not (self.offset_row <= row < self.offset_row + self.START_ROWS): continue
        #     if not (self.offset_col <= col < self.offset_col + self.START_ROWS): continue
        #     x, y = (col - self.offset_col) * self.FIELD_SIZE, (row - self.offset_row) * self.FIELD_SIZE
        #
        #     pct_to_blit = None
        #     if bonus_type == Slow.__name__:
        #         pct_to_blit = self.__slow_image
        #     elif bonus_type == BonusMoney.__name__:
        #         pct_to_blit = self.__money_image
        #     elif bonus_type == BonusLife.__name__:
        #         pct_to_blit = self.__live_image
        #     elif bonus_type == Nuke.__name__:
        #         pct_to_blit = self.__nuke_image
        #
        #     if pct_to_blit is not None: self.screen.blit(pct_to_blit, (x, y))

    def draw_monsters(self):
        for pos, monster in self.on_load_monsters.items():
            if not monster: continue
            row, col = pos
            if not (self.offset_row <= row < self.offset_row + self.START_ROWS): continue
            if not (self.offset_col <= col < self.offset_col + self.START_ROWS): continue
            x, y = (col - self.offset_col) * self.FIELD_SIZE, (row - self.offset_row) * self.FIELD_SIZE

            pct_to_blit = None
            if monster == MonsterTypes.SKULL:
                pct_to_blit = self.__skull_image
            elif monster == MonsterTypes.GHOST:
                pct_to_blit = self.__ghost_image
            elif monster == MonsterTypes.DEMON:
                pct_to_blit = self.__demon_image
            if pct_to_blit is not None: self.screen.blit(pct_to_blit, (x, y))

        for pos, flag in self.monster_spawn_tiles.items():
            if not flag: continue
            row, col = pos
            if not (self.offset_row <= row < self.offset_row + self.START_ROWS): continue
            if not (self.offset_col <= col < self.offset_col + self.START_ROWS): continue
            x, y = (col - self.offset_col) * self.FIELD_SIZE, (row - self.offset_row) * self.FIELD_SIZE
            self.screen.blit(self.__egg_image, (x, y))

    def add_bonus_prob(self, bonus_type, probability_string):
        def is_valid_int(string):
            try:
                int(string)  # Próba konwersji na int
                return True  # Konwersja zakończona sukcesem
            except ValueError:
                return False

        if not is_valid_int(probability_string): return False

        # To uncomment
        # if self.table[(row, col)].TYPE != TileType.VOID: return False

        self.bonus_probabilities[bonus_type] = (int(probability_string), None)

    def change_in_hand(self, new_hand):
        self.in_hand = new_hand
        if self.in_hand == INHAND.SLOW:
            self.add_bonus_prob(Slow.__name__, self.slow_input.text)
        elif self.in_hand == INHAND.BONUSLIFE:
            self.add_bonus_prob(BonusLife.__name__, self.live_input.text)

        elif self.in_hand == INHAND.NUKE:
            self.add_bonus_prob(Nuke.__name__, self.nuke_input.text)

        elif self.in_hand == INHAND.BONUSMONEY:
            self.add_bonus_prob(BonusMoney.__name__, self.money_input.text)

    def check_and_save(self):
        is_ok = True
        if self.pacman_x is None or self.pacman_y is None:
            is_ok = False
            self.dialog_text.txt = "Error! Place the Pacman to save the map"

        if len(self.bonus_probabilities) == 0:
            is_ok = False
            self.dialog_text.txt = "Error! Place some bonus to save the map"

        if len(self.monster_spawn_tiles) == 0:
            is_ok = False
            self.dialog_text.txt = "Error! Place some monster eggs to save the map"

        if len(self.on_load_monsters) == 0:
            is_ok = False
            self.dialog_text.txt = "Error! Place some monsters to save the map"
        if is_ok:
            self.change_creator_scene(ICREATOR.SAVE)
        else:
            self.change_creator_scene(ICREATOR.DIALOG)



    def add_new_column(self):
        for row in range(self.rows):
            self.table[(row, self.cols)] = Tile(TileType.VOID)

        self.cols += 1
        self.offset_col += 1

    def add_new_row(self):
        for col in range(self.cols):
            self.table[(self.rows, col)] = Tile(TileType.VOID)

        self.rows += 1
        self.offset_row += 1

    def change_creator_scene(self, new_scene):
        self.level_creator_scene = new_scene

    def change_drawing_boundaries(self, new_boundary):
        def between(x, a, b):
            return a <= x <= b

        if between(self.offset_row + new_boundary[0], 0, self.rows - self.START_ROWS):
            self.offset_row += new_boundary[0]

        if between(self.offset_col + new_boundary[1], 0, self.cols - self.START_ROWS):
            self.offset_col += new_boundary[1]

        print(self.rows, self.offset_row, self.cols, self.offset_col)

    def save_to_file(self):
        pathname = "resources/usermaps/"+self.map_name.text+".txt"
        file = open(pathname, "w")

        # row, col
        file.write(f'{self.rows} {self.cols}\n')

        # Table
        for row in range(self.rows):
            for col in range(self.cols):
                file.write(f'{self.table[(row, col)].TYPE.value} ')
            file.write('\n')

        # Pacman coord
        file.write(f'{(self.pacman_y,self.pacman_x)}\n')

        # Dots and RedBall
        for pos, placed in self.dots.items():
            if not placed: continue
            row, col = pos
            file.write(f'{(row, col)};')
        file.write("\n")

        for pos, placed in self.red_dots.items():
            if not placed: continue
            row, col = pos
            file.write(f'{(row, col)};')
        file.write("\n")

        for bonus_type, spec in self.bonus_probabilities.items():
            prob, pol = spec
            file.write(f'{(bonus_type, prob, pol)};')
        file.write('\n')

        # Monsters
        for pos, monster_type in self.on_load_monsters.items():
            if not monster_type: continue
            row, col = pos
            file.write(f'{monster_type.value, row, col};')
        file.write('\n')

        for pos, flag in self.monster_spawn_tiles.items():
            if not flag: continue
            row, col = pos
            print("monster spawn tiles = ", pos)
            file.write(f'{row, col};')

        file.close()
        self.init_map()

    def return_to_menu_routine(self):
        self.init_map()
        Scene.change_menu_scene(SceneTypes.MAIN)

    def load_white_dots(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.is_occupied(row, col):
                    self.dots[(row, col)] = True



