from Enums import Direction as Direction
from Enums.Direction import *
import pygame


#Nadrzedna klasa dla wszystkich mobow w grze (potworki + pacman)
class MapElement:
    def __init__(self,POS_X,POS_Y,FIELD_SIZE,C_CHECKER,MAP):
        self.POS_X = POS_X
        self.POS_Y = POS_Y
        self.SOLID_AREA = pygame.Rect(5, 5, FIELD_SIZE-10, FIELD_SIZE-10)
        self._C_CHECKER = C_CHECKER
        self._MAP = MAP
        self._direction = Direction.RIGHT
        self.MAX_SPEED = 3 #maksymalna (domyslna) szybkosc
        self._speed = 0 #aktualna szybkosc
        self._cur_sprite_nr = 0 #nr aktualnego sprite'a do wyswietlenia
        self.MAX_SPRITE_NR = 1 #Wzkazuje ile sprite'ow ma dany element


    def get_image_path(self): #abstract
        pass

    def __str__(self): #abstract
        pass

    #PONIZSZE METODY PUBLICZNE

    def get_pos_x(self):
        return self.POS_X

    def get_pos_y(self):
        return self.POS_Y

    def get_direction(self):
        return self._direction

    def set_speed(self,speed):
        self._speed = speed

    def get_speed(self):
        return self._speed

