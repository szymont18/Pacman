from enum import Enum
import datetime


class HARDNESS(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class GameSpec:
    def __init__(self):
        self.game_tps = 120

        self.hardness = HARDNESS.MEDIUM

        self.start_level = None
        self.to_play_level = None

        self.start_game = False
        self.lives = 3
        self.score = 0

        self.time = 0
        self.time_counter = 0

        self.level_status = None

    def set_start_level(self, start_level):
        self.start_level = start_level
        self.to_play_level = start_level
        self.start_game = True

    def get_start_game_status(self):
        return self.start_game

    def set_hardness_ratio(self, ratio):
        if 0 <= ratio < 1 / 3:
            self.hardness = HARDNESS.EASY
        elif 1 / 3 <= ratio < 2 / 3:
            self.hardness = HARDNESS.MEDIUM
        else:
            self.hardness = HARDNESS.HARD

    def get_hardness(self):
        return self.hardness

    def get_level_to_play(self):
        return self.to_play_level

    def get_lives(self): return self.lives

    def get_score(self): return self.score

    def set_lives(self, lives): self.lives = lives

    def set_score(self, score): self.score = score

    def set_start_game(self, start_game): self.start_game = start_game

    def increment_lvl(self): self.to_play_level += 1

    def get_str_time(self):
        delta = datetime.timedelta(seconds=self.time)
        str_time = str(delta).split(".")[0]  # delete milisecond

        length_delta = 8 - len(str_time)
        if length_delta > 0:
            str_time = '0' * length_delta + str_time

        return str_time

    def reset(self):
        self.start_level = None
        self.to_play_level = None

        self.start_game = False
        self.lives = 3
        self.score = 0
        self.level_status = None

        self.time = 0
        self.time_counter = 0

    def increment_time(self, time): self.time += time

    def get_start_level(self): return self.start_level

