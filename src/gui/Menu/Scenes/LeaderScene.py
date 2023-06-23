import pygame

from ..Components.Image import Image
from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *
import pandas as pd


class SORTED(Enum):
    SCORE = 1
    TIME = 2


class LeaderScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        self.rectangle_window = pygame.rect.Rect((100, 200), (514, 500))
        self.title = TextArea(Vector2d(200, 150), 414, 100, "Leader Board", self.screen, rgb=(247, 245, 245))

        self.sort_by = SORTED.SCORE
        self.sort_by_score_button = Button(Vector2d(285, 100), 214, 50, "Score", self.screen,
                                           lambda: self.change_sort_way(SORTED.SCORE))

        self.sort_by_time_button = Button(Vector2d(285, 400), 214, 50, "Time", self.screen,
                                          lambda: self.change_sort_way(SORTED.TIME))

        self.return_button = Button(Vector2d(600, 200), 314, 50, "Return", screen,
                                    lambda: Scene.change_menu_scene(SceneTypes.MAIN))

        self.leader_board = pd.read_csv("resources/leader_board.csv", sep=",")

        self.leader_board_time = self.leader_board.sort_values(by="Time", inplace=False)
        self.leader_board_time.reset_index(drop=True)
        self.leader_board_time["ind"] = [i + 1 for i in range(len(self.leader_board_time))]
        new_order = ["ind", "Nick", "Score", "Time"]
        self.leader_board_time = self.leader_board_time[new_order]

        self.leader_board_score = self.leader_board.sort_values(by="Score", ascending=False, inplace=False)
        self.leader_board_score.reset_index(drop=True)
        self.leader_board_score["ind"] = [i + 1 for i in range(len(self.leader_board_score))]
        self.leader_board_score = self.leader_board_score[new_order]

        self.leader_board = self.leader_board_score.iloc[:10]
        self.leader_board_pos = Vector2d(335, 112)

        self.col_width = [20,150, 150, 150]

        self.row_height = 26

        self.up_image = Image(Vector2d(335, 586), 24, 2 * self.row_height, self.screen, "resources/menu/up.png")
        self.down_image = Image(Vector2d(543, 586), 24, 2 * self.row_height, self.screen, "resources/menu/down.png")

        self.up_button = Button(Vector2d(335, 586), 24, 2 * self.row_height, "", screen,
                                lambda: self.change_offset(self.offset - 1))

        self.down_button = Button(Vector2d(543, 586), 24, 2 * self.row_height, "", screen,
                                  lambda: self.change_offset(self.offset + 1))

        self.font = pygame.font.SysFont("comicsanms", 15)

        self.offset = 0

    def draw(self, mouse):

        pygame.draw.rect(self.screen, 'black', self.rectangle_window)
        self.title.draw()

        self.return_button.draw()
        self.sort_by_score_button.draw()
        self.sort_by_time_button.draw()
        self.down_button.draw()
        self.up_button.draw()
        self.up_image.draw()
        self.down_image.draw()

        self.up_button.is_clicked(mouse)
        self.down_button.is_clicked(mouse)
        self.sort_by_time_button.is_clicked(mouse)
        self.return_button.is_clicked(mouse)
        self.sort_by_score_button.is_clicked(mouse)

        self.draw_leader_board()

    def change_sort_way(self, new_way):

        self.leader_board = pd.read_csv("resources/leader_board.csv", sep=",")

        self.leader_board_time = self.leader_board.sort_values(by="Time", inplace=False)
        self.leader_board_time.reset_index(drop=True)
        self.leader_board_time["ind"] = [i + 1 for i in range(len(self.leader_board_time))]
        new_order = ["ind","Nick", "Score","Time"]
        self.leader_board_time = self.leader_board_time[new_order]
        self.leader_board_score = self.leader_board.sort_values(by="Score", ascending=False, inplace=False)
        self.leader_board_score.reset_index(drop=True)
        self.leader_board_score["ind"] = [i + 1 for i in range(len(self.leader_board_score))]
        self.leader_board_score = self.leader_board_score[new_order]

        self.sort_by = new_way

        if self.sort_by == SORTED.SCORE:
            self.leader_board = self.leader_board_score[:10]

        else:
            self.leader_board = self.leader_board_time[:10]

    def draw_leader_board(self):
        x, y = self.leader_board_pos.get_coords()
        cnt = 0
        for i, row in self.leader_board.iterrows():
            for j, item in enumerate(row):
                cell_x = x + sum(self.col_width[:j])
                cell_y = y + cnt * self.row_height
                pygame.draw.rect(self.screen, (247, 245, 245), (cell_x, cell_y, self.col_width[j], self.row_height), 1)

                text = self.font.render(str(item), True, (247, 245, 245))
                text_rect = text.get_rect(center=(cell_x + self.col_width[j] // 2, cell_y + self.row_height // 2))
                self.screen.blit(text, text_rect)
            cnt += 1

    def change_offset(self, new_offset):
        if new_offset < 0 or new_offset + 10 > len(self.leader_board_score): return

        self.offset = new_offset
        if self.sort_by == SORTED.SCORE:
            self.leader_board = self.leader_board_score[self.offset: self.offset + 10]
        else:
            self.leader_board = self.leader_board_time[self.offset: self.offset + 10]
