import time
from abc import abstractmethod


class Item:
    def __init__(self, POS_X, POS_Y, MAX_SPRITE_NR, SOLID_AREA, MAP, MAX_PICK_UP_SPRITE_NR):
        # Item's attributes can be public because thera are constants
        self.POS_X = POS_X
        self.POS_Y = POS_Y
        self._sprite_nr = 1
        self.MAX_SPRITE_NR = MAX_SPRITE_NR  # Number of textures
        self.MAX_PICK_UP_SPRITE_NR = MAX_PICK_UP_SPRITE_NR  # Number of textures where item is picked up
        self.SOLID_AREA = SOLID_AREA

        # self.is_active = is_active

        self._is_eaten = False  # Was it eaten (opposite of is_active)

        self._MAP = MAP
        self.__ready_to_remove = False  # If an item sets itself ready_to_remove -
        # the engine will know to tell the map to remove it
        # self._ENGINE = None

        # Timer
        self._last_sprite_chg = time.time()
        self.SPRITE_CHG_TIME = 0.5  # How much texture change under normal conditions
        self.SPRITE_PICKUP_CHG_TIME = 0.2  # How much texture change when the item was picked up

    def get_ready_to_remove(self):
        return self.__ready_to_remove

    @abstractmethod
    def get_image_path(self):  # abstract
        pass

    # def set_activity(self, new):
    #    self.is_active = new

    def get_is_eaten(self):
        return self._is_eaten

    @abstractmethod
    def __str__(self):
        pass

    def update(self):
        time_now = time.time()
        if not self._is_eaten and time_now - self._last_sprite_chg > self.SPRITE_CHG_TIME:
            self._sprite_nr = (self._sprite_nr + 1) % (self.MAX_SPRITE_NR + 1)
            self._sprite_nr = self._sprite_nr if self._sprite_nr != 0 else 1
            self._last_sprite_chg = time.time()

        elif self._is_eaten and time_now - self._last_sprite_chg > self.SPRITE_PICKUP_CHG_TIME:
            self._sprite_nr += 1
            self._last_sprite_chg = time.time()

            if self._sprite_nr >= self.MAX_PICK_UP_SPRITE_NR:
                # self._MAP.remove_item(self)
                self.__ready_to_remove = True

    # Inform that item has got eaten
    def got_eaten(self):
        self._is_eaten = True
        self._sprite_nr = 1
