from abc import ABC, abstractmethod

from Enums import Direction as Direction
from Enums.Direction import *
import pygame
import time


#Nadrzedna klasa dla wszystkich mobow w grze (potworki + pacman)
class MapElement(ABC):
    def __init__(self,POS_X,POS_Y,FIELD_SIZE,C_CHECKER,MAP,SPRITE_CHG_TIME,ENGINE):
        self.POS_X = POS_X
        self.POS_Y = POS_Y
        self.SOLID_AREA = pygame.Rect(5, 5, FIELD_SIZE - 10, FIELD_SIZE - 10)
        self._C_CHECKER = C_CHECKER
        self._MAP = MAP
        self._direction = Direction.RIGHT
        self.MAX_SPEED = 3 #maksymalna (domyslna) szybkosc
        self._speed = 0 #aktualna szybkosc
        self.FIELD_SIZE = FIELD_SIZE
        self.SPRITE_CHG_TIME = SPRITE_CHG_TIME
        self._is_newborn = True
        self._is_killed = False #tj. potwor zjadl pacmana lub pacman potwora i leci animacja smierci
        self._last_sprite_chg = time.time()
        self._cur_sprite_nr = 1  # nr aktualnego sprite'a do wyswietlenia
        self._ENGINE = ENGINE

    @abstractmethod
    def get_image_path(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    #PONIZSZE METODY PUBLICZNE
    def get_pos_x(self):
        return self.POS_X

    def get_pos_y(self):
        return self.POS_Y

    def set_pos_x(self,pos_x):
        self.POS_X = pos_x

    def set_pos_y(self,pos_y):
        self.POS_Y = pos_y

    def get_direction(self):
        return self._direction

    def set_speed(self,speed):
        self._speed = speed

    def get_speed(self):
        return self._speed

    def update(self):
        #Jesli jest dojrzaly i zyje to sie porusza
        if(not self._is_newborn and not self._is_killed):
            self.move() #Wolana jest metoda .move w odpowiedniej klasie dziedziczacej
        elif self._is_newborn: #Jesli jest nowonarodzony to beda animacje rodzenia sie
            time_now = time.time()
            if time_now - self._last_sprite_chg> self.SPRITE_CHG_TIME:
                self._cur_sprite_nr +=1
                self._last_sprite_chg = time_now
                if self._cur_sprite_nr == 6:
                    self._is_newborn = False
                    self._cur_sprite_nr = 1
                    self.set_speed(self.MAX_SPEED)
        elif self._is_killed:
            time_now = time.time()
            if time_now - self._last_sprite_chg > self.SPRITE_CHG_TIME:
                self._cur_sprite_nr += 1
                self._last_sprite_chg = time_now
                if self._cur_sprite_nr == 5:
                    self._ENGINE.map_element_died(self)
        else:
            raise Exception("niezdefiniowane zachowanie w MapElement/upate")


    def kill(self): #metoda zabija Postac (potworka lub pacmana)
        if self._is_killed: return #jesli juz nie zyje to nie zabijaj go od nowa (ten if jest po to zeby nie resetowala sprite_nr jak ktos stanie na nim znowu)
        self._is_killed = True
        self._speed = 0
        self._cur_sprite_nr = 1