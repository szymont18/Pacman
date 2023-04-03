import time

import pygame,sys

from Items.BonusLife import BonusLife
from Items.BonusMoney import BonusMoney
from Utility.CollisionChecker import *
from MapElements.Pacman import Pacman
from Items.Item import Item
from Items.Dot import Dot
from Items.RedBall import RedBall
from random import randint

class Engine(object):
    def __init__(self,MAP,MAX_ROW,MAX_COL,APP,KEYH,FIELD_SIZE):
        pygame.init()

        #STALE
        self.TPS = 120 #tickrate
        self.STARTING_LIVES = 3
        self.MAX_ENEMIES_ALIVE = 4 # Gdy __enemies_alive == MAX_ENEMIES_ALIVE to potwory sie nie respia
        self.BONUS_APEAR_TIME = 3600 # Co 30 sekund (3600/TPS) pojawia sie na mapie losowy bonus
        self.BONUS_DISAPEAR_TIME = 1200 # Po 10 sekundach jesli nie podniesiony - znika
        self.__tps_delta = 0.0
        self.__tps_clock = pygame.time.Clock()

        #Rozgrywka
        self.__lives = 3
        self.__score = 0
        self.__dots_eaten = 0
        self.__enemies_alive = 0
        self.__keep_running = True # czy silnik ma dalej pracowac
        self.__pacman = None # uchwyt do pacmana

        self.__APP = APP
        self.MAX_COL = MAX_COL
        self.MAX_ROW = MAX_ROW
        self.__MAP = MAP
        self.FIELD_SIZE = FIELD_SIZE
        self.__C_CHECKER = CollisionChecker(self, self.__MAP) # mechanizm odpowiadajacy za wykrywanie kolizji i podnoszenie przedmiotow
        self.spawn_pacman(KEYH)
        self.__KEYH = KEYH

    def spawn_pacman(self, KEYH):
        spawn_x = self.__MAP.get_pacman_spawn_x()
        spawn_y = self.__MAP.get_pacman_spawn_y()

        self.__pacman = Pacman(spawn_x, spawn_y, self.FIELD_SIZE, KEYH, self.__C_CHECKER, self.__MAP, self)

    def run(self):
        time_keeper, last_time = 0, time.time()
        while self.__keep_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)  # potem mozna przerobic zeby wolalo metode Menu
                elif event.type == pygame.KEYDOWN:
                    self.__KEYH.key_pressed(event)
                elif event.type == pygame.KEYUP:
                    self.__KEYH.key_released(event)

            self.__tps_delta += self.__tps_clock.tick() / 1000.0
            time_keeper += self.__tps_clock.tick() / 1000.0

            while self.__tps_delta > 1 / self.TPS:

                self.update()
                self.__tps_delta -= 1 / self.TPS

            time_keeper = time.time()
            if time_keeper - last_time > 5:
                last_time = time.time()
                self.spawn_bonus()

            # Drawing
            self.draw()
            pygame.display.flip()

    def update(self):
        self.__pacman.move()

    def draw(self):
        self.__APP.clear_map() #czysci ekran
        self.__APP.draw_map(self.__MAP)
        self.__APP.draw_items(self.__MAP)
        self.__APP.draw_map_element(self.__pacman)
        self.__APP.draw_pacman_status(self.__lives, self.__score)

    def picked_up(self, item: Item):
        if isinstance(item, Dot):
            self.__dots_eaten += 1
        elif isinstance(item, RedBall):
            self.__score += 100
        elif isinstance(item, BonusLife):
            self.__lives += 1
        elif isinstance(item, BonusMoney):
            self.__score += 10_000

        # print("Actual lifes = ", self.__lives)
        # print("Dots_eaten = ", self.__dots_eaten)
        # print("Score = ", self.__score)

    def random_choice(self, prob: int):
        prob = 100 * prob
        choice = randint(1, 101)
        if choice <= prob:
            return True
        return False

    def spawn_bonus(self): #respi pieniazki, serduszki
        for bonus_type, information in self.__MAP.bonus_probability.items():
            probability, coordinates = information
            if self.random_choice(probability):
                new_bonus = bonus_type(coordinates[1], coordinates[0], probability)

                new_bonus.set_activity(True)
                self.__MAP.add_item(new_bonus)
                return




