from MapElements.MapElement import MapElement
from Enums import Direction as Direction
from Enums.Direction import *

class Pacman(MapElement):
    def __init__(self,POS_X,POS_Y,FIELD_SIZE,KEY_HANDLER,C_CHECKER,MAP,ENGINE):
        super().__init__(POS_X,POS_Y,FIELD_SIZE,C_CHECKER,MAP)
        self.__KEY_HANDLER = KEY_HANDLER
        self.__ENGINE = ENGINE

        #Gdy uzytkownik wcisnal klawisz, ale pacman nie moze aktualnie wykonac skretu to tu jest przechowywana
        #informacje gdzie skrecic gdy nadazy sie taka mozliwosc
        self.__next_turn = None #Docelowo przechowuje Direction

    #Override
    def __str__(self):
        return "P "+self._direction.__str__()

    #Override
    def get_image_path(self):
        if(self._direction == Direction.UP):
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

            if self._C_CHECKER.can_move(self,self._direction): #jesli pacman moze isc w nowym kierunku
                self.set_speed(self.MAX_SPEED)  # wprawiamy pacmana w ruch

        #Tutaj nastepuje ruszenie pacmana
        if self._direction == Direction.UP:
            self.POS_Y -= self._speed
        elif self._direction == Direction.DOWN:
            self.POS_Y += self._speed
        elif self._direction == Direction.LEFT:
            self.POS_X -= self._speed
        else:
            self.POS_X += self._speed

        #Po ruchu sprawdzamy czy weszlismy na item
        item = self._C_CHECKER.check_for_items(self)

        if item != None:
            print("Picked up")
            self._MAP.remove_item(item) #usuwamy item z mapy aby sie nie wyswietlal
            self.__ENGINE.picked_up(item) #informujemy silnik zeby uruchomil bonusy podniesionego przedmiotu

        else:
            print("No item")





