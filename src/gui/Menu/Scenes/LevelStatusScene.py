from src.MapElements.Vector2d import Vector2d
from ..Components.Image import Image
from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *


from enum import Enum

from ..Components.TextInput import TextInput


class STATUS(Enum):
    LVL_WIN = 1
    LVL_LOSE = 2
    GAME_WIN = 3


class LevelStatusScene(Scene):

    def __init__(self, screen):
        super().__init__(screen)

        self.rectangle = pygame.rect.Rect((100, 200), (514, 400))

        self.status = None

        # Win level
        self.lvl_win1 = TextArea(Vector2d(200, 100), 514, 100, f'Congratulation !!!', self.screen)
        self.lvl_win2 = TextArea(Vector2d(350, 250), 214, 50, f'Level passed!', self.screen, font_size=45,
                                 rgb=(247, 245, 245))
        self.lvl_win3 = TextArea(Vector2d(450, 250), 214, 50, f'Press space to continue', self.screen, font_size=45,
                                 rgb=(247, 245, 245))

        # Lose level
        self.lvl_defeat1 = TextArea(Vector2d(200, 100), 514, 100, f'Defeat :(', self.screen, rgb=(184, 6, 26))
        self.lvl_defeat2 = TextArea(Vector2d(350, 250), 214, 50, f'Level lost!', self.screen, font_size=45,
                                    rgb=(247, 245, 245))
        self.lvl_defeat3 = TextArea(Vector2d(450, 250), 214, 50, f'Press space to continue', self.screen, font_size=45,
                                    rgb=(247, 245, 245))

        # Win Game
        self.game_win1 = TextArea(Vector2d(200, 100), 514, 100, f'Congratulations!!!', self.screen)
        self.game_win2 = TextArea(Vector2d(350, 250), 214, 50, f'You win the game!', self.screen, font_size=45,
                                  rgb=(247, 245, 245))
        self.game_win3 = TextArea(Vector2d(450, 250), 214, 50, f'Fill your nickname and press space to save and exit',
                                  self.screen, font_size=32, rgb=(247, 245, 245))

        self.leader_board_actualise = TextInput(Vector2d(600, 250), 214, 50, screen, font_size=50)

    def draw(self, mouse):
        pygame.draw.rect(self.screen, "black", self.rectangle, 0, 5)
        if self.status == STATUS.LVL_WIN:
            self.lvl_win1.draw()
            self.lvl_win2.draw()
            self.lvl_win3.draw()

        elif self.status == STATUS.LVL_LOSE:
            self.lvl_defeat1.draw()
            self.lvl_defeat2.draw()
            self.lvl_defeat3.draw()

        else:
            if Scene.GAME_SPEC.get_start_level() == 0:
                self.leader_board_actualise.is_clicked(mouse)
                self.leader_board_actualise.update()
                self.game_win3.draw()
                self.leader_board_actualise.draw()

            self.game_win1.draw()
            self.game_win2.draw()


    def change_game_status(self, new_status):
        self.status = new_status
