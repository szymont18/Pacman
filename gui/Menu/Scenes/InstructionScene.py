import pygame

from .GhostBonusScene import GhostBonusScene
# TODO: Bonuses and scenes for all bonuses and ghosts

from ..Components.Image import Image
from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *
from enum import Enum


class IScene(Enum):
    GAMEPLAY = 1
    PACMAN = 2
    BONUS = 3
    GHOST = 4
    G_SKULL = 5
    G_DEMON = 6
    B_DOT = 7
    B_RED_BALL = 8
    B_MONEY = 9
    B_LIFE = 10


class InstructionScene(Scene):

    def __init__(self, screen):
        super().__init__(screen)

        # Black background
        self.rectangle_window = pygame.rect.Rect((100, 200), (514, 500))
        self.instruction_scene_pointer = IScene.GAMEPLAY
        self.prev_instruction_scene = None

        self.title = TextArea(Vector2d(200, 200), 314, 100, "Instructions", self.screen, rgb=(247, 245, 245))

        # Main areas - { game_play, pacman, ghost, bonus }
        self.game_play = TextArea(Vector2d(285, 200), 314, 100, "Gameplay", self.screen, rgb=(247, 245, 245),
                                  font_size=30)

        self.pacman = TextArea(Vector2d(285, 200), 314, 100, "Pacman", self.screen, rgb=(247, 245, 245),
                               font_size=30)

        self.ghost = TextArea(Vector2d(285, 200), 314, 100, "Ghosts", self.screen, rgb=(247, 245, 245),
                              font_size=30)

        self.bonus = TextArea(Vector2d(285, 200), 314, 100, "Bonuses", self.screen, rgb=(247, 245, 245),
                              font_size=30)

        # Explanation for main areas
        self.text1 = "The player controls a yellow ball - the titular Pac-Man - through a maze filled with white " \
                     "balls. The condition for progressing to the next level is to eat all the balls. Additionally, " \
                     "the player must avoid the ghosts that move around the map. There are also larger (red) balls on " \
                     "the board that allow the player to eat the enemies for a short period of time. Eating a ghost " \
                     "results in additional points. Special symbols appear on the board that award bonuses or rewards " \
                     "when eaten. The objective of the game is to pass through all the stages"

        self.text2 = "The creation shown in the pictures below is Pac-Man. To move Pac-Man, use the arrow keys on the " \
                     "keyboard. To eat a ghost or a bonus, simply run into it on the game board (no need to press " \
                     "anything)."

        self.text3 = "This is a group of ghosts that will make your gameplay difficult. Each of them has a separate " \
                     "hunting tactic."

        self.text4 = "These are bonuses that will allow you to gain extra points or abilities."

        # Text areas
        self.game_play_plain_text = TextArea(Vector2d(375, 150), 414, 200, self.text1, self.screen, rgb=(247, 245, 245),
                                             font_size=25, center_pos=False)

        self.pacman_plain_text = TextArea(Vector2d(375, 150), 414, 200, self.text2, self.screen, rgb=(247, 245, 245),
                                          font_size=25, center_pos=False)

        self.ghost_plain_text = TextArea(Vector2d(375, 150), 414, 200, self.text3, self.screen, rgb=(247, 245, 245),
                                         font_size=25, center_pos=False)

        self.bonus_plain_text = TextArea(Vector2d(375, 150), 414, 200, self.text4, self.screen, rgb=(247, 245, 245),
                                         font_size=25, center_pos=False)

        self.pacman_move_text = TextArea(Vector2d(550, 150), 50, 50, "Move", self.screen, rgb=(247, 245, 245),
                                         font_size=25)
        self.pacman_win_text = TextArea(Vector2d(550, 332), 50, 50, "Win", self.screen, rgb=(247, 245, 245),
                                        font_size=25)
        self.pacman_die_text = TextArea(Vector2d(550, 514), 50, 50, "Die", self.screen, rgb=(247, 245, 245),
                                        font_size=25)

        # Switch button - buttons that allow to switch between main areas ( for example from pacman to ghost )
        self.pacman_button = Button(Vector2d(600, 400), 214, 50, "Pacman", screen,
                                    lambda: self.change_instruction_scene(IScene.PACMAN))

        self.pacman_button2 = Button(Vector2d(600, 100), 214, 50, "Pacman", screen,
                                     lambda: self.change_instruction_scene(IScene.PACMAN))

        self.return_button = Button(Vector2d(600, 100), 214, 50, "Return", screen,
                                    lambda: Scene.change_menu_scene(SceneTypes.MAIN))

        self.game_play_button = Button(Vector2d(600, 100), 214, 50, "Gameplay", screen,
                                       lambda: self.change_instruction_scene(IScene.GAMEPLAY))

        self.ghost_button = Button(Vector2d(600, 400), 214, 50, "Ghosts", screen,
                                   lambda: self.change_instruction_scene(IScene.GHOST))

        self.ghost_button2 = Button(Vector2d(600, 100), 214, 50, "Ghosts", screen,
                                    lambda: self.change_instruction_scene(IScene.GHOST))

        self.bonus_button = Button(Vector2d(600, 400), 214, 50, "Bonuses", screen,
                                   lambda: self.change_instruction_scene(IScene.BONUS))

        # Images to make instruction more attractive

        self.pacman_move = [Image(Vector2d(500, 150), 50, 50, screen, f'resources/pacman/P_left_{i}.png') for i in
                            range(1, 5)]
        self.pacman_win = [Image(Vector2d(500, 332), 50, 50, screen, f'resources/pacman/P_WIN_{i}.png') for i in
                           range(1, 5)]
        self.pacman_die = [Image(Vector2d(500, 514), 50, 50, screen, f'resources/pacman/P_DIE_{i}.png') for i in
                           range(1, 6)]

        self.skull = [Image(Vector2d(500, 150), 50, 50, screen, f'resources/skull/S_LEFT_{i}.png') for i in
                      range(1, 5)]

        self.demon = [Image(Vector2d(500, 332), 50, 50, screen, f'resources/demon/D_left_{i}.png') for i in
                      range(1, 5)]

        self.dot = [Image(Vector2d(500, 167), 50, 50, screen, f'resources/items/Dot.png')]

        self.red_ball = [Image(Vector2d(500, 277), 50, 50, screen, f'resources/items/RedBall{i}.png') for i in range(1, 5)]

        self.money = [Image(Vector2d(500, 387), 50, 50, screen, f'resources/items/BonusMoney{i}.png') for i in range(1, 3)]

        self.life = [Image(Vector2d(500, 497), 50, 50, screen, f'resources/items/BonusLife{i}.png') for i in range(1, 5)]



        # Specification for further explanation of game element - ghost (their tactics), bonus (what they do)

        self.skull_button = Button(Vector2d(550, 145), 60, 50, "Skull", screen,
                                   lambda: self.change_instruction_scene(IScene.G_SKULL), font_size=25)

        self.demon_button = Button(Vector2d(550, 327), 60, 50, "Demon", screen,
                                   lambda: self.change_instruction_scene(IScene.G_DEMON), font_size=25)

        self.dot_button = Button(Vector2d(550, 162), 60, 50, "Dot", screen,
                                   lambda: self.change_instruction_scene(IScene.B_DOT), font_size=25)

        self.red_ball_button = Button(Vector2d(550, 272), 60, 50, "Red Ball", screen,
                                   lambda: self.change_instruction_scene(IScene.B_RED_BALL), font_size=25)

        self.money_button = Button(Vector2d(550, 382), 60, 50, "Money", screen,
                                   lambda: self.change_instruction_scene(IScene.B_MONEY), font_size=25)

        self.life_button = Button(Vector2d(550, 492), 60, 50, "Life", screen,
                                   lambda: self.change_instruction_scene(IScene.B_LIFE), font_size=25)

        self.demon_plain_text = "Demon is one of the smarter enemies. It can recognize Pacman and follow him if he is" \
                                "in the same column or row. It is very difficult to shake off, so try not to " \
                                "encounter it " \
                                "during gameplay"
        self.skull_plain_text = "The Skull is a less intelligent enemy. It moves randomly around the map and is not " \
                                "interested in fighting until you come into contact with it."

        self.life_plain_text = "After eating this bonus, the player receives an extra life. They can have an infinite "\
                               "number of lives, but only 5 lives will be displayed on the health bar."

        self.money_plain_text = "After eating this bonus, the player receives an additional 10,000 points."

        self.red_ball_plain_text = "After eating this bonus, the player (Pacman) scares all the opponents. As a " \
                                   "result, they become vulnerable for 5 seconds and can be defeated (eaten). For " \
                                   "each defeated monster, the player receives an additional 1000 points."

        self.dot_plain_text = "Dots are the basic bonuses that appear on the map. The player must eat all of them to " \
                              "progress to the next level (and ultimately win the game)."

        self.exp_scene_map = {IScene.G_DEMON: GhostBonusScene(self.screen, "Demon", self.demon_plain_text,
                                                              [f'resources/demon/D_left_{i}.png' for i in range(1, 5)]),
                              IScene.G_SKULL: GhostBonusScene(self.screen, "Skull", self.skull_plain_text,
                                                              [f'resources/skull/S_LEFT_{i}.png' for i in range(1, 5)]),
                              IScene.B_LIFE: GhostBonusScene(self.screen, "Life", self.life_plain_text,
                                                              [f'resources/items/BonusLife{i}.png' for i in range(1, 5)]),
                              IScene.B_DOT: GhostBonusScene(self.screen, "Dot", self.dot_plain_text,
                                                              [f'resources/items/Dot.png']),
                              IScene.B_RED_BALL: GhostBonusScene(self.screen, "Red Ball", self.red_ball_plain_text,
                                                              [f'resources/items/RedBall{i}.png' for i in range(1, 5)]),
                              IScene.B_MONEY: GhostBonusScene(self.screen, "Money", self.money_plain_text,
                                                              [f'resources/items/BonusMoney{i}.png' for i in range(1, 3)])
                              }

        # Return to one of the specific explanation
        self.return_from_exp = Button(Vector2d(600, 200), 314, 50, "Return", screen,
                                      lambda: self.change_instruction_scene(self.prev_instruction_scene))

    def draw(self, mouse):
        pygame.draw.rect(self.screen, 'black', self.rectangle_window)
        self.title.draw()

        if self.instruction_scene_pointer == IScene.GAMEPLAY:
            self.game_play.draw()
            self.game_play_plain_text.draw()
            self.pacman_button.draw()
            self.return_button.draw()

            self.return_button.is_clicked(mouse)
            self.pacman_button.is_clicked(mouse)

        elif self.instruction_scene_pointer == IScene.PACMAN:
            self.pacman.draw()
            self.pacman_plain_text.draw()
            self.game_play_button.draw()
            self.ghost_button.draw()

            self.pacman_win[self.sprite_nr % len(self.pacman_win)].draw()
            self.pacman_die[self.sprite_nr % len(self.pacman_die)].draw()
            self.pacman_move[self.sprite_nr % len(self.pacman_move)].draw()

            self.pacman_move_text.draw()
            self.pacman_win_text.draw()
            self.pacman_die_text.draw()

            self.ghost_button.is_clicked(mouse)
            self.game_play_button.is_clicked(mouse)

        elif self.instruction_scene_pointer == IScene.GHOST:
            self.ghost.draw()
            self.ghost_plain_text.draw()
            self.pacman_button2.draw()
            self.bonus_button.draw()
            self.demon_button.draw()
            self.skull_button.draw()
            self.demon[self.sprite_nr % len(self.demon)].draw()
            self.skull[self.sprite_nr % len(self.skull)].draw()

            self.demon_button.is_clicked(mouse)
            self.skull_button.is_clicked(mouse)
            self.pacman_button2.is_clicked(mouse)
            self.bonus_button.is_clicked(mouse)

        elif self.instruction_scene_pointer == IScene.BONUS:
            self.bonus.draw()
            self.ghost_button2.draw()
            self.bonus_plain_text.draw()

            self.life[self.sprite_nr % len(self.life)].draw()
            self.dot[self.sprite_nr % len(self.dot)].draw()
            self.red_ball[self.sprite_nr % len(self.red_ball)].draw()
            self.money[self.sprite_nr % len(self.money)].draw()

            self.life_button.draw()
            self.dot_button.draw()
            self.red_ball_button.draw()
            self.money_button.draw()

            self.life_button.is_clicked(mouse)
            self.dot_button.is_clicked(mouse)
            self.red_ball_button.is_clicked(mouse)
            self.money_button.is_clicked(mouse)
            self.ghost_button2.is_clicked(mouse)

        else:
            self.exp_scene_map[self.instruction_scene_pointer].draw(mouse)
            self.return_from_exp.draw()
            self.return_from_exp.is_clicked(mouse)

        # Actualise sprites
        self.sprite_blink()

    def change_instruction_scene(self, new_scene):
        self.prev_instruction_scene = self.instruction_scene_pointer
        self.instruction_scene_pointer = new_scene

