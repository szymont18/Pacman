from ..MapElements.MapElement import MapElement
from ..Enums import Direction as Direction
from ..Enums.Direction import *
import pygame
import time
#from MapElements import MapElement
#from MapElement import MapElement


class Pacman(MapElement):
    def __init__(self, POS_X, POS_Y, FIELD_SIZE, KEY_HANDLER, C_CHECKER, MAP, ENGINE, SPRITE_CHG_TIME,
                 SPRITE_ON_DEATH_CHG_TIME,
                 BLINK_TIME, EAT_TIME_FACE, MAX_DIE_SPRITES, MAX_SPAWN_SPRITES):
        super().__init__(POS_X, POS_Y, FIELD_SIZE, C_CHECKER, MAP, SPRITE_CHG_TIME, SPRITE_ON_DEATH_CHG_TIME, ENGINE,
                         MAX_DIE_SPRITES, MAX_SPAWN_SPRITES)
        self.__KEY_HANDLER = KEY_HANDLER
        self.__won = False  # Has Pacman won the game already

        # If User push the button but Pacman can not move to specified directory
        # this directory is stored in this variable
        self.__next_turn = None  # Stores Direction variable

        # Variables responsible for loses hearth
        self.__hurt = False
        self.__visible = True
        self.__hurt_clock = -float('inf')
        self.__last_blink = -float('inf')
        self.__BLINK_TIME = BLINK_TIME
        self.__played_epilog_animation = False #Level should end when pacman finishes his animation

        # Variables responsible for sprites changing
        self.__EAT_TIME_FACE = EAT_TIME_FACE
        self.__last_eat_change = -float('inf')

    # Override
    def __str__(self):
        return "P " + self._direction.__str__()

    # Override
    def get_image_path(self):
        if self._is_newborn:
            return f"resources/pacman/P_SPAWN_{self._cur_sprite_nr}.png"

        if self.__won:
            return f"resources/pacman/P_WIN_{self._cur_sprite_nr}.png"

        if self._is_killed:
            return f"resources/pacman/P_DIE_{self._cur_sprite_nr}.png"

        if self.__hurt and self._cur_sprite_nr == 2:
            return f"resources/tiles/VOID.png"

        if self._direction == Direction.UP:
            return f'resources/pacman/P_up_{self._cur_sprite_nr}.png'
        elif self._direction == Direction.DOWN:
            return f'resources/pacman/P_down_{self._cur_sprite_nr}.png'
        elif self._direction == Direction.LEFT:
            return f'resources/pacman/P_left_{self._cur_sprite_nr}.png'
        elif self._direction == Direction.RIGHT:
            return f'resources/pacman/P_right_{self._cur_sprite_nr}.png'
        else:
            raise Exception(self.get_direction() + " is not a valid direction")

    def move(self):
        # If KEY_HANDLER has a click queued, we set PacMan to turn in that direction at the next opportunity
        if self.__KEY_HANDLER.up_pressed:
            self.__next_turn = Direction.UP
        elif self.__KEY_HANDLER.down_pressed:
            self.__next_turn = Direction.DOWN
        elif self.__KEY_HANDLER.left_pressed:
            self.__next_turn = Direction.LEFT
        elif self.__KEY_HANDLER.right_pressed:
            self.__next_turn = Direction.RIGHT

        # If it cannot turn, it continues in the same direction or stands still
        if not self._C_CHECKER.can_move(self, self.__next_turn):

            # but if it cannot go on in the same direction, it must stop
            if not self._C_CHECKER.can_move(self, self._direction):
                self.set_speed(0)  # Pacman stopped
        else:
            self._direction = self.__next_turn  # Pacman turns
            self.__next_turn = None  # Used the turn

            if self._C_CHECKER.can_move(self, self._direction):  # If Pacman can move to the new directory
                self.set_speed(self.MAX_SPEED)  # Pacman start to move

        # Pacman moving
        if self._direction == Direction.UP:
            self.set_pos_y((self.POS_Y - self._speed) % (self._MAP.MAX_COL * self._MAP.FIELD_SIZE))
        elif self._direction == Direction.DOWN:
            self.set_pos_y((self.POS_Y + self._speed) % (self._MAP.MAX_COL * self._MAP.FIELD_SIZE))
        elif self._direction == Direction.LEFT:
            self.set_pos_x((self.POS_X - self._speed) % (self._MAP.MAX_COL * self._MAP.FIELD_SIZE))
        else:
            self.set_pos_x((self.POS_X + self._speed) % (self._MAP.MAX_COL * self._MAP.FIELD_SIZE))

        # Check if we crossed the item
        item = self._C_CHECKER.check_for_items(self)

        if item is not None and not item.get_is_eaten() and self._C_CHECKER.crosses_with_pacman(item):
            self._ENGINE.picked_up(item)  # Inform engine to take the bonus

    def win(self):
        self.__won = True
        self._speed = 0
        self._cur_sprite_nr = 1
        self._last_sprite_chg = time.time()

    def update(self):
        if self.__won:
            time_now = time.time()
            if time_now - self._last_sprite_chg > self.SPRITE_CHG_TIME:
                if self._cur_sprite_nr < 4:
                    self._cur_sprite_nr += 1
                    self._last_sprite_chg = time_now
                else:
                    self.__played_epilog_animation = True
        else:
            super().update()

        if self.__hurt and not self._is_killed and not self.__won:
            if pygame.time.get_ticks() - self.__last_blink > 100:
                self.__visible = False if self.__visible else True
                self.__last_blink = pygame.time.get_ticks()

        # Po 5 sekundach Pacman znów staje się vulnerable
        if pygame.time.get_ticks() - self.__hurt_clock > self.__BLINK_TIME * 1000:
            self.__hurt = False
            self.__visible = True

    def is_hurt(self):
        return self.__hurt

    def set_hurt(self, flag):
        self.__hurt = flag

        if self.__hurt:
            self.__hurt_clock = pygame.time.get_ticks()

    def is_visible(self):
        return self.__visible

    def set_visible(self, visible):
        self.__visible = visible

    def get_played_epilog_animation(self):
        return self.__played_epilog_animation

    def set_played_epilog_animation(self,val):
        self.__played_epilog_animation = val