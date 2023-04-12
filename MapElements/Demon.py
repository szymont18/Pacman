import random

from MapElements.MapElement import MapElement
from Enums import Direction as Direction
from Enums.Direction import *
import numpy as np
import time
import pygame

class Demon(MapElement):
    def __init__(self,POS_X,POS_Y,FIELD_SIZE,C_CHECKER,MAP,ENGINE,MONSTER_ID,GROW_TIME):
        super().__init__(POS_X, POS_Y, FIELD_SIZE, C_CHECKER, MAP,GROW_TIME,ENGINE)
        self.MONSTER_ID = MONSTER_ID #Unikalne Id potwora ulatwiajace silnikowi wyciaganie ich z Dicta


        #W przyszlosci warto przerobic growstage na cur_sprite_nr jak beda teksturki gotowe

    #Override
    def __str__(self):
        return "S "+self._direction.__str__()

    #Override
    def get_image_path(self):
        if self._is_newborn:
            return f"resources/demon/D_EGG_{self._cur_sprite_nr}.png"

        if (self._direction == Direction.UP):
            return "resources/demon/D_UP_1.png"
        elif self._direction == Direction.DOWN:
            return "resources/demon/D_DOWN_1.png"
        elif self._direction == Direction.LEFT:
            return "resources/demon/D_LEFT_1.png"
        elif self._direction == Direction.RIGHT:
            return "resources/demon/D_RIGHT_1.png"
        else:
            raise Exception(self.get_direction() + " is not a valid direction")





    def move(self):
        #Jesli czaszka nie moze dalej isc prosto to losuje nowy kierunek ruchu
        if ( not self._C_CHECKER.can_move(self, self._direction)):

            directions = [Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN]
            random.shuffle(directions) #wprowadzamy losowosc

            for direction in directions: #sprawdzamy kolejne kierunki i potwor skreca w pierwszy mozliwy
               if self._C_CHECKER.can_move(self,direction):
                   self._direction = direction  # zmiana kierunku
                   break


        #Tutaj nastepuje ruszenie potworka (wiemy na tym etapie ze moze tam isc)
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
            self._ENGINE.kill_pacman()
