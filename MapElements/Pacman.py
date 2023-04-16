from MapElements.MapElement import MapElement
from Enums import Direction as Direction
from Enums.Direction import *
import pygame
import time

class Pacman(MapElement):
    def __init__(self,POS_X,POS_Y,FIELD_SIZE,KEY_HANDLER,C_CHECKER,MAP,ENGINE,SPRITE_CHG_TIME,SPRITE_ON_DEATH_CHG_TIME):
        super().__init__(POS_X, POS_Y, FIELD_SIZE, C_CHECKER, MAP,SPRITE_CHG_TIME,SPRITE_ON_DEATH_CHG_TIME,ENGINE)
        self.__KEY_HANDLER = KEY_HANDLER
        self.__won = False #czy pacman wygral juz gre


        #Gdy uzytkownik wcisnal klawisz, ale pacman nie moze aktualnie wykonac skretu to tu jest przechowywana
        #informacje gdzie skrecic gdy nadazy sie taka mozliwosc
        self.__next_turn = None #Docelowo przechowuje Direction

    #Override
    def __str__(self):
        return "P "+self._direction.__str__()

    #Override
    def get_image_path(self):
        if self._is_newborn:
            return f"resources/pacman/P_SPAWN_{self._cur_sprite_nr}.png"

        if self.__won:
            return f"resources/pacman/P_WIN_{self._cur_sprite_nr}.png"

        if self._is_killed:
            return f"resources/pacman/P_DIE_{self._cur_sprite_nr}.png"

        if (self._direction == Direction.UP):
            return "resources/pacman/P_up_1.png"
        elif self._direction == Direction.DOWN:
            return "resources/pacman/P_down_1.png"
        elif self._direction == Direction.LEFT:
            return "resources/pacman/P_left_1.png"
        elif self._direction == Direction.RIGHT:
            return "resources/pacman/P_right_1.png"
        else:
            raise Exception(self.get_direction() + " is not a valid direction")

    def move(self):
        #Jesli KEY_HANDLER ma w kolejce klikniecie to ustawiamy ze przy najblizszej okazji PacMan ma skrecic w dana strone
        if self.__KEY_HANDLER.up_pressed:
            self.__next_turn = Direction.UP
        elif self.__KEY_HANDLER.down_pressed:
            self.__next_turn = Direction.DOWN
        elif self.__KEY_HANDLER.left_pressed:
            self.__next_turn = Direction.LEFT
        elif self.__KEY_HANDLER.right_pressed:
            self.__next_turn = Direction.RIGHT

        # Jesli nie moze skrecic to idzie dalej w tym samym kierunku badz stoi
        if not self._C_CHECKER.can_move(self,self.__next_turn):

            #jesli jednak nie moze isc dalej w tym samym kierunku to musi stac
            if(not self._C_CHECKER.can_move(self,self._direction)):
                self.set_speed(0) #zatrzymanie pacmana
        else:
            self._direction = self.__next_turn #pacman skreca
            self.__next_turn = None #wykorzystal skret

            if self._C_CHECKER.can_move(self, self._direction): #jesli pacman moze isc w nowym kierunku
                self.set_speed(self.MAX_SPEED)  # wprawiamy pacmana w ruch

        #Tutaj nastepuje ruszenie pacmana
        if self._direction == Direction.UP:
            self.set_pos_y( (self.POS_Y - self._speed)% (self._MAP.MAX_COL * self._MAP.FIELD_SIZE))
        elif self._direction == Direction.DOWN:
            self.set_pos_y( (self.POS_Y + self._speed)% (self._MAP.MAX_COL * self._MAP.FIELD_SIZE))
        elif self._direction == Direction.LEFT:
            self.set_pos_x( (self.POS_X - self._speed)% (self._MAP.MAX_COL * self._MAP.FIELD_SIZE))
        else:
            self.set_pos_x( (self.POS_X + self._speed)% (self._MAP.MAX_COL * self._MAP.FIELD_SIZE))


        #Po ruchu sprawdzamy czy weszlismy na item
        item = self._C_CHECKER.check_for_items(self)

        if item != None and item.is_active:
           # print("Picked up")
            self._MAP.remove_item(item) # usuwamy item z mapy aby sie nie wyswietlal
            self._ENGINE.picked_up(item) # informujemy silnik zeby uruchomil bonusy podniesionego przedmiotu

    def win(self):
        self.__won = True
        self._speed = 0
        self._cur_sprite_nr = 1
        self._last_sprite_chg = time.time()

    def update(self):
        if self.__won:
            time_now = time.time()
            if time_now - self._last_sprite_chg > self.SPRITE_CHG_TIME and self._cur_sprite_nr < 4:
                self._cur_sprite_nr += 1
                self._last_sprite_chg = time_now
        else:
            super().update()





