import random

from MapElements.MapElement import MapElement
from Enums import Direction as Direction
from Enums.Direction import *
import numpy as np
import time
import pygame


class Skull(MapElement):
    def __init__(self, POS_X, POS_Y, FIELD_SIZE, C_CHECKER, MAP, ENGINE, MONSTER_ID, GROW_TIME, DIE_TIME,
                 MAX_DIE_SPRITES, MAX_SPAWN_SPRITES):
        super().__init__(POS_X, POS_Y, FIELD_SIZE, C_CHECKER, MAP, GROW_TIME, DIE_TIME, ENGINE, MAX_DIE_SPRITES,
                         MAX_SPAWN_SPRITES)
        self.MONSTER_ID = MONSTER_ID  # Unique ID
        self.__is_vulnerable = False  # Pacman can not eat Skull unless he previously has eaten red dot

        # In the future, it's worth changing the growstage to cur_sprite_nr when the textures are ready

    # Override
    def __str__(self):
        return "S " + self._direction.__str__()

    # Override
    def get_image_path(self):
        if self._is_newborn:
            return f"resources/skull/S_EGG_{self._cur_sprite_nr}.png"
        elif self._is_killed:
            return f"resources/skull/S_DIE_{self._cur_sprite_nr}.png"
        elif self.__is_vulnerable:
            return f"resources/skull/V_{self._direction}_{self._cur_sprite_nr}.png"

        return f"resources/skull/S_{self._direction}_{self._cur_sprite_nr}.png"

    def move(self):
        # If the skull can no longer go straight, it randomizes a new direction of movement
        if not self._C_CHECKER.can_move(self, self._direction):

            directions = [Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN]
            random.shuffle(directions)  # Randomness

            for direction in directions:  # Check new directions
                if self._C_CHECKER.can_move(self, direction):
                    self._direction = direction  # Change the direction
                    break

        # Here the monster moves (we know at this stage that it can go there)
        if self._direction == Direction.UP:
            self.POS_Y -= self._speed
            self.POS_Y = self.POS_Y % (self._MAP.MAX_COL * self._MAP.FIELD_SIZE)
        elif self._direction == Direction.DOWN:
            self.POS_Y += self._speed
            self.POS_Y = self.POS_Y % (self._MAP.MAX_COL * self._MAP.FIELD_SIZE)
        elif self._direction == Direction.LEFT:
            self.POS_X -= self._speed
            self.POS_X = self.POS_X % (self._MAP.MAX_ROW * self._MAP.FIELD_SIZE)
        else:
            self.POS_X += self._speed
            self.POS_X = self.POS_X % (self._MAP.MAX_ROW * self._MAP.FIELD_SIZE)

        if self._C_CHECKER.crosses_with_pacman(self):
            if self.__is_vulnerable:
                self.kill()
            else:
                self._ENGINE.hurt_pacman()

    def change_vulnerability(self, val: bool):
        self.__is_vulnerable = val
        self._cur_sprite_nr = 1
