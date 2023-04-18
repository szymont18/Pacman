import random

from Enums import Direction as Direction
from Enums.Direction import *
from MapElements.MapElement import MapElement


class Demon(MapElement):
    def __init__(self, POS_X, POS_Y, FIELD_SIZE, C_CHECKER, MAP, ENGINE, MONSTER_ID, GROW_TIME, DIE_TIME,
                 MAX_DIE_SPRITES, MAX_SPAWN_SPRITES):
        super().__init__(POS_X, POS_Y, FIELD_SIZE, C_CHECKER, MAP, GROW_TIME, DIE_TIME, ENGINE, MAX_DIE_SPRITES,
                         MAX_SPAWN_SPRITES)
        self.MONSTER_ID = MONSTER_ID  # Unique ID

        # In the future, it's worth changing the growstage to cur_sprite_nr when the textures are ready

    # Override
    def __str__(self):
        return "S " + self._direction.__str__()

    # Override
    def get_image_path(self):
        if self._is_newborn:
            return f"resources/demon/D_EGG_{self._cur_sprite_nr}.png"

        return f"resources/demon/D_{self._direction}_{self._cur_sprite_nr}.png"

    def move(self):
        # If demon is in the same column or row as Pacman he changes directory
        if not self._ENGINE.is_pacman_hurt():
            pacman_position = self._ENGINE.get_pacman_pos()
            field_size = self._ENGINE.FIELD_SIZE

            demon_row, demon_col = self.POS_Y // field_size, self.POS_X // field_size
            pacman_row, pacman_col = pacman_position[1] // field_size, pacman_position[0] // field_size
            new_direction = None

            if demon_col == pacman_col:
                if demon_row < pacman_row:
                    new_direction = Direction.DOWN
                elif demon_row > pacman_row:
                    new_direction = Direction.UP

            if demon_row == pacman_row:
                if demon_col < pacman_col:
                    new_direction = Direction.RIGHT
                elif demon_col > pacman_col:
                    new_direction = Direction.LEFT

            if new_direction is not None and self._C_CHECKER.can_move(self, new_direction):
                self._direction = new_direction

        # If skull can not go straight it go to random direction which is available
        if not self._C_CHECKER.can_move(self, self._direction):

            directions = [Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN]
            random.shuffle(directions)  # Randomness
            for direction in directions:  # Iterate through directions to check which is available
                if self._C_CHECKER.can_move(self, direction):
                    self._direction = direction  # Change direction
                    break

        # Monster is moving ( we know that this directory is correct)
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
            self._ENGINE.hurt_pacman()
