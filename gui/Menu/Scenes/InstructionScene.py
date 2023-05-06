import pygame
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


class InstructionScene(Scene):

    def __init__(self, screen):
        super().__init__(screen)

        self.rectangle_window = pygame.rect.Rect((100, 200), (514, 500))
        self.instruction_scene_pointer = IScene.GAMEPLAY

        self.title = TextArea(Vector2d(200, 200), 314, 100, "Instructions", self.screen, rgb=(247, 245, 245))

        self.game_play = TextArea(Vector2d(285, 200), 314, 100, "Gameplay", self.screen, rgb=(247, 245, 245),
                                  font_size=30)

        self.pacman = TextArea(Vector2d(285, 200), 314, 100, "Pacman", self.screen, rgb=(247, 245, 245),
                               font_size=30)

        self.ghost = TextArea(Vector2d(285, 200), 314, 100, "Ghosts", self.screen, rgb=(247, 245, 245),
                              font_size=30)

        self.bonus = TextArea(Vector2d(285, 200), 314, 100, "Bonuses", self.screen, rgb=(247, 245, 245),
                              font_size=30)

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

        self.skull_text = TextArea(Vector2d(550, 150), 50, 50, "Skull", self.screen, rgb=(247, 245, 245),
                                   font_size=25)
        self.demon_text = TextArea(Vector2d(550, 332), 50, 50, "Demon", self.screen, rgb=(247, 245, 245),
                                   font_size=25)

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

            self.pacman_win[0].draw()
            self.pacman_die[0].draw()
            self.pacman_move[0].draw()

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
            self.demon[0].draw()
            self.skull[0].draw()
            self.demon_text.draw()
            self.skull_text.draw()

            self.pacman_button2.is_clicked(mouse)
            self.bonus_button.is_clicked(mouse)

        else:
            self.bonus.draw()
            self.ghost_button2.draw()
            self.bonus_plain_text.draw()

            self.ghost_button2.is_clicked(mouse)

    def change_instruction_scene(self, new_scene):
        self.instruction_scene_pointer = new_scene
