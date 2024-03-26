from abc import ABC, abstractmethod

from ..Enums import Direction as Direction
from ..Enums.Direction import *
import pygame
import time
#from MapElements.Pacman import Pacman
#from MapElements.Pacman import *


class MapElement(ABC):
    def __init__(self, POS_X, POS_Y, FIELD_SIZE, C_CHECKER, MAP, SPRITE_CHG_TIME, SPRITE_ON_DEATH_CHG_TIME, ENGINE,
                 MAX_DIE_SPRITES, MAX_SPAWN_SPRITES,MAX_SPEED=3):
        self.POS_X = POS_X
        self.POS_Y = POS_Y
        self.SOLID_AREA = pygame.Rect(5, 5, FIELD_SIZE - 10, FIELD_SIZE - 10)
        self._C_CHECKER = C_CHECKER
        self._MAP = MAP
        self._direction = Direction.RIGHT
        self.MAX_SPEED = MAX_SPEED  # Max and casual speed
        self._speed = 0  # Actual speed
        self.FIELD_SIZE = FIELD_SIZE
        self.SPRITE_CHG_TIME = SPRITE_CHG_TIME
        self.SPRITE_ON_DEATH_CHG_TIME = SPRITE_ON_DEATH_CHG_TIME
        self.MAX_DIE_SPRITES = MAX_DIE_SPRITES
        self.MAX_SPAWN_SPRITES = MAX_SPAWN_SPRITES
        self._is_newborn = True
        self._is_killed = False  # Somebody kills his enemy
        self._last_sprite_chg = time.time()
        self._cur_sprite_nr = 1  # Actual sprite to display
        self._ENGINE = ENGINE

    @abstractmethod
    def get_image_path(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def move(self):
        pass

    # Public methods
    def get_pos_x(self):
        return self.POS_X

    def get_pos_y(self):
        return self.POS_Y

    def set_pos_x(self, pos_x):
        self.POS_X = pos_x

    def set_pos_y(self, pos_y):
        self.POS_Y = pos_y

    def get_direction(self):
        return self._direction

    def set_speed(self, speed):
        self._speed = speed

    def get_speed(self):
        return self._speed

    def get_is_alive(self):
        return not self._is_killed

    def get_is_newborn(self):
        return self._is_newborn

    def update(self):
        # If it is not new_born and is alived
        if not self._is_newborn and not self._is_killed:
            self.move()  # In every in the inheriting class, the move class is called

            time_now = time.time()
            if time_now - self._last_sprite_chg > self.SPRITE_CHG_TIME / 3:
                self._cur_sprite_nr = (self._cur_sprite_nr + 1) % 5
                self._cur_sprite_nr = self._cur_sprite_nr if self._cur_sprite_nr != 0 else 1
                self._last_sprite_chg = time_now

        elif self._is_newborn:  # If he is newborn, there will be birth animations
            time_now = time.time()
            if time_now - self._last_sprite_chg > self.SPRITE_CHG_TIME:
                self._cur_sprite_nr += 1
                self._last_sprite_chg = time_now
                if self._cur_sprite_nr == self.MAX_SPAWN_SPRITES:
                    self._is_newborn = False
                    self._cur_sprite_nr = 1
                    self.set_speed(self.MAX_SPEED)

        elif self._is_killed:
            time_now = time.time()
            if time_now - self._last_sprite_chg > self.SPRITE_ON_DEATH_CHG_TIME:
                self._cur_sprite_nr = (self._cur_sprite_nr + 1) % 6
                self._cur_sprite_nr = self._cur_sprite_nr if self._cur_sprite_nr != 0 else 1
                self._last_sprite_chg = time_now
                if self._cur_sprite_nr == self.MAX_DIE_SPRITES:
                    self._ENGINE.map_element_died(self)
                    #if isinstance(self,Pacman): #Pacman has to finish his animation before game ends
                    #    self.set_played_epilog_animation(True)

    def kill(self):  # kill map Element
        if self._is_killed: return  # if he's already dead, don't kill him again
        self._is_killed = True
        self._speed = 0
        self._cur_sprite_nr = 1

    def get_solid_area(self):
        return self.SOLID_AREA