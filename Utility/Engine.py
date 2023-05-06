import random
import time
import pygame, sys
from Items.BonusLife import BonusLife
from Items.BonusMoney import BonusMoney
from Utility.CollisionChecker import *
from MapElements.Pacman import Pacman
from Items.Item import Item
from Items.Dot import Dot
from Items.RedBall import RedBall
from random import randint
from numpy.random import randint
from Enums.MonsterTypes import *
from MapElements.Skull import *
from MapElements.Demon import *
from Utility.KeyHandler import *
from MapElements.Pacman import *


class Engine(object):
    def __init__(self, MAP, MAX_ROW, MAX_COL, APP, KEYH, FIELD_SIZE):
        # pygame.init() # Moved to App.py -> launch function

        # CONSTANTS
        self.TPS = 120  # tick rate
        self.STARTING_LIVES = 3
        self.MAX_MONSTERS_ALIVE = 4  # When __enemies_alive == MAX_ENEMIES_ALIVE then monsters don't spawn
        self.MONSTER_APEAR_TIME = 5  # Every 5 seconds a new monster appears as long as the monster limit isn't exceeded
        self.GROW_TIME = 0.5  # Every 0.5 seconds the newborn map_element grows in size until it becomes an adult
        # after 5 boosts (for pacman and monsters)
        self.DIE_TIME = 0.2  # Every 0.2 seconds map_element dies animation
        self.BONUS_APEAR_TIME = 10  # Every 10 seconds a random bonus appears on the map
        self.BONUS_DISAPEAR_TIME = 5  # After 10 seconds if not picked up - disappears
        self.CAN_EAT_SKULLS_DURATION = 5  # Pacman can eat a skull for 10 seconds (when he picks up a red orb)
        self.BLINK_TIME = 5  # For 5 seconds, Pacman cannot cuff again
        self.ITEM_BLINK_TIME = 0.2  # Every 0.2 seconds items blink
        self.EAT_TIME_FACE = 0.1  # How much Pacman  mouth moves

        # GAME
        self.__lives = 3
        self.__score = 0
        self.__dots_eaten = 0
        self.__can_eat_skulls = False
        self.__can_eat_skulls_remaining_time = -float('inf')

        # The flag is there to keep the monster dict from resizing when the engine iterates over it
        # The engine, after iterating through the dictionary, will unlock the ability to delete from the dictionary
        # self.__can_remove_monster = False

        self.__keep_running = True  # if engine has to works
        self.__game_on = True  # if somebody win
        self.__game_won = False  # if pacman win
        self.__is_paused = False
        self.__pacman = None  # handler to Pacman

        self.__monsters = dict()  # Dict to store monsters
        self.next_monster_id = 0  # Next spawn monster ID
        self.__monsters_alive = 0
        self.__is_monsters_vulnerable = False

        self.__tps_delta = 0.0
        self.__tps_clock = pygame.time.Clock()
        self.__APP = APP
        self.MAX_COL = MAX_COL
        self.MAX_ROW = MAX_ROW
        self.__MAP = MAP
        self.FIELD_SIZE = FIELD_SIZE
        self.__C_CHECKER = CollisionChecker(self, self.__MAP)  # Responsible for moving and lifting items
        self.spawn_pacman(KEYH)
        self.__KEYH = KEYH

    def spawn_pacman(self, KEYH):
        spawn_x = self.__MAP.get_pacman_spawn_x()
        spawn_y = self.__MAP.get_pacman_spawn_y()
        self.__pacman = Pacman(spawn_x, spawn_y, self.FIELD_SIZE, KEYH, self.__C_CHECKER, self.__MAP, self,
                               self.GROW_TIME, self.DIE_TIME, self.BLINK_TIME, self.EAT_TIME_FACE, 5, 5)

    def spawn_monster(self, init_monster_type=None, init_pos_x=None, init_pos_y=None):
        monster = None

        # If a monster has been indicated and where it is to spawn, we do not draw a monster, we only place it once
        if init_monster_type is not None and init_pos_x is not None and init_pos_y is not None:
            # print("juz predefined")
            if init_monster_type == MonsterTypes.SKULL:
                monster = Skull(init_pos_x, init_pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self,
                                self.next_monster_id, self.GROW_TIME, self.DIE_TIME, 4, 5)
            elif init_monster_type == MonsterTypes.DEMON:
                monster = Demon(init_pos_x, init_pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self,
                                self.next_monster_id, self.GROW_TIME, self.DIE_TIME, 4, 5)

        else:  # Random Monster
            monster_types = self.__MAP.POSSIBLE_MONSTERS
            n1 = len(monster_types)
            random_id = randint(0, n1)
            monster_type = monster_types[random_id]  # This monster

            # print("spawn_monster")
            # print(monster_type)

            spawn_tiles = self.__MAP.MONSTER_SPAWN_TILES
            n2 = len(spawn_tiles)
            random_id = randint(0, n2)
            spawn_tile = spawn_tiles[random_id]  # Coordinates

            # monster = None
            pos_x = spawn_tile[0] * self.FIELD_SIZE
            pos_y = spawn_tile[1] * self.FIELD_SIZE

            if monster_type == MonsterTypes.SKULL:
                monster = Skull(pos_x, pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self, self.next_monster_id,
                                self.GROW_TIME, self.DIE_TIME, 4, 5)

        self.__monsters[self.next_monster_id] = monster
        # print(self.__MONSTERS[self.next_monster_id])
        self.next_monster_id += 1
        self.__monsters_alive += 1

    def remove_monster(self, monster_id):
        self.__monsters[monster_id] = None
        # self.__monsters.pop(monster_id)
        self.__monsters_alive -= 1
        # After killing monster pacman score is incremented
        self.__score += 1000
        # self.__safe_to_remove_monster = False
        # print("usunieto")

    def spawn_onload_monsters(self):
        # print("spawning onload monsters")
        monsters = self.__MAP.get_onload_monsters()

        for monster_type, (row, col) in monsters:
            self.spawn_monster(monster_type, col * self.FIELD_SIZE, row * self.FIELD_SIZE)

    # All things that should be set after pacman win
    def pacman_won(self):
        # self.__pacman.set_speed(0)
        self.update()
        self.__pacman.win()  # will cause pacman to stop and play the joy of winning animation
        self.__game_on = False
        self.__game_won = True
        self.__pacman.set_visible(True)

        self.__MAP.clear_items()
        self.__monsters = dict()
        self.__monsters_alive = 0

        print("Wygrales")
        print("Nacisnij spacje aby przejsc do nastepnego poziomu")

    def pacman_lost(self):
        self.__game_on = False
        self.__game_won = False

        # self.__monsters = dict()
        self.__monsters_alive = 0

        print("Przegrales")
        print("Nacisnij spacje aby kontynuowac")

    #  Shut the main loop of the engine
    def shut_down(self):
        self.__keep_running = False

    def run(self):

        # time_keeper, last_time = 0, time.time()

        time_keeper = 0
        last_bonus_spawn_time = time.time()
        last_monster_spawn_time = time.time()

        self.spawn_onload_monsters()  # Spawn few monsters on the start

        while self.__keep_running:
            # print(self.__MAP.get_total_dots())
            # SEKCJA EVENTOW
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)  # TODO: call method menu
                elif event.type == pygame.KEYDOWN:
                    self.__KEYH.key_pressed(event)
                elif event.type == pygame.KEYUP:
                    self.__KEYH.key_released(event)

            self.__tps_delta += self.__tps_clock.tick() / 1000.0
            time_keeper += self.__tps_clock.tick() / 1000.0

            # Until  neither side won
            if self.__game_on:

                # Moving map elements
                while self.__tps_delta > 1 / self.TPS:
                    self.update()
                    self.__tps_delta -= 1 / self.TPS

                # TEST
                # if self.__dots_eaten == 5:
                #    self.pacman_won()

                if self.__dots_eaten == self.__MAP.get_total_dots():
                    self.update()
                    self.pacman_won()

                # Respawn monster and items
                time_keeper = time.time()
                if time_keeper - last_bonus_spawn_time > self.BONUS_APEAR_TIME:
                    last_bonus_spawn_time = time.time()
                    self.spawn_bonus()

                if (time_keeper - last_monster_spawn_time > self.MONSTER_APEAR_TIME
                        and self.__monsters_alive < self.MAX_MONSTERS_ALIVE):
                    last_monster_spawn_time = time.time()
                    self.spawn_monster()

                pygame_time = pygame.time.get_ticks()
                if (self.__is_monsters_vulnerable
                        and pygame_time - self.__can_eat_skulls_remaining_time > self.CAN_EAT_SKULLS_DURATION * 1000):
                    self.make_skulls_predators()

            else:  # if somebody wins

                if self.__KEYH.space_pressed:
                    self.__keep_running = False

            # Drawing
            self.draw()
            pygame.display.flip()

        # End game - win / lose
        if self.__game_won:  # Win
            return 10
        elif not self.__game_on:  # Lose
            return -10

        return 0  # Other

    def update(self):
        self.__pacman.update()
        # self.__can_remove_monster = False
        # Moving monsters
        to_remove = []

        for monster_id in self.__monsters.keys():
            if self.__monsters[monster_id] is None:
                to_remove.append(monster_id)
            else:
                self.__monsters[monster_id].update()
        for monster_id in to_remove:
            self.__monsters.pop(monster_id)

        ########################################

        to_remove = []
        items = self.__MAP.get_items()

        for item_key in items.keys():
            if items[item_key].get_ready_to_remove():
                to_remove.append(item_key)
            else:
                items[item_key].update()

        for item_key in to_remove:
            self.__MAP.remove_item(items[item_key])

    # self.__can_remove_monster = True

    def draw(self):
        self.__APP.clear_map()  # Clear map
        self.__APP.draw_map(self.__MAP)
        self.__APP.draw_items(self.__MAP)

        if self.__pacman.is_visible():
            self.__APP.draw_map_element(self.__pacman)

        for monster_id in self.__monsters.keys():
            if self.__monsters[monster_id] is not None:
                self.__APP.draw_map_element(self.__monsters[monster_id])

        self.__APP.draw_pacman_status(self.__lives, self.__score)

        if not self.__game_on and self.__game_won:
            self.__APP.draw_win_level()

        if not self.__game_on and not self.__game_won:
            self.__APP.draw_lose_level()

    # We tell the engine to assign the bonuses associated with picking up the item and the item itself will inform
    # about picking it up (Item will play pick up animations)
    def picked_up(self, item: Item):
        if isinstance(item, Dot):
            self.__dots_eaten += 1
            self.__score += 100

        elif isinstance(item, RedBall):
            # print("podniesiono redBall")
            self.__score += 200
            self.make_skulls_vulnerable()
        elif isinstance(item, BonusLife):
            # print("podniesiono serduszko")
            self.__lives += 1
        elif isinstance(item, BonusMoney):
            # print("podniesiono kaske")
            self.__score += 10_000

        item.got_eaten()

    def random_choice(self, chances, bonus):
        return random.choices(bonus, weights=chances, k=1)[0]

    # Spawn money, hearths ...
    def spawn_bonus(self):
        chances = [information[0] * 100 for _, information in self.__MAP.bonus_probability.items()]
        coordinates = [information[1] for _, information in self.__MAP.bonus_probability.items()]
        bonus = [bonus_type for bonus_type, information in self.__MAP.bonus_probability.items()]

        indexes = [i for i in range(len(chances))]
        index = self.random_choice(chances, indexes)

        actual_coordinate = coordinates[index]
        actual_bonus = bonus[index]
        actual_probability = chances[index]

        if actual_coordinate is None:
            actual_coordinate = self.__MAP.get_random_spawn_place()
        new_bonus = actual_bonus(actual_coordinate[1], actual_coordinate[0], actual_probability, self.__MAP)
        # new_bonus.set_activity(True)
        self.__MAP.add_item(new_bonus)
        return

        # OLD system
        # for bonus_type, information in self.__MAP.bonus_probability.items():
        #     probability, coordinates = information
        #     if coordinates is None:
        #         coordinates = self.__MAP.get_random_spawn_place()
        #     if self.random_choice(probability):
        #         new_bonus = bonus_type(coordinates[1], coordinates[0], probability)
        #
        #         new_bonus.set_activity(True)
        #         self.__MAP.add_item(new_bonus)
        #         return

    # The method works a bit like notification of the observer after the death of a mob -
    # it is used to clean up after it
    def map_element_died(self, element: MapElement):
        if isinstance(element, Pacman):  # Pacman die
            self.__lives = 0  # It's going to zero (???) TODO : Test if nessesary
            self.pacman_lost()

        else:  # We know it is monster
            self.remove_monster(element.MONSTER_ID)

    # To remove (???)
    # Metoda sluzy do zabicia moba, ktory odegra animacja smierci a nastepnie zawola metode map_element_died
    # informujac silnik ze mozna go usunac z mapy
    # def kill_map_element(self,element):
    #    element.kill()

    # A method preferred by spirits that will cross a pacman to hurt or kill him
    def hurt_pacman(self):
        # print("pacman zabijany, pacman_is_hurt", self.__pacman.is_hurt())
        if not self.__pacman.is_hurt():
            self.__pacman.set_hurt(True)
            self.__lives -= 1

        if self.__lives == 0:
            self.__pacman.kill()

    def get_pacman_solid_area(self):
        # print("printuje")
        # print(self.__pacman.SOLID_AREA)
        return self.__pacman.SOLID_AREA

    def get_pacman_pos(self):
        return self.__pacman.get_pos_x(), self.__pacman.get_pos_y()

    def is_pacman_hurt(self):
        return self.__pacman.is_hurt()

    def make_skulls_vulnerable(self):
        # print(self.__monsters)
        print("SKULLS ARE VULNERABLE")

        for monster_id in self.__monsters:
            monster = self.__monsters[monster_id]
            if isinstance(monster, Skull) and monster.get_is_alive() and not monster.get_is_newborn():
                self.__monsters[monster_id].change_vulnerability(True)

        self.__can_eat_skulls_remaining_time = pygame.time.get_ticks()
        self.__is_monsters_vulnerable = True

    def make_skulls_predators(self):
        print("SKULLS ARE AGAIN PREDATORS")

        for monster_id in self.__monsters:
            monster = self.__monsters[monster_id]
            if isinstance(monster, Skull) and monster.get_is_alive() and not monster.get_is_newborn():
                self.__monsters[monster_id].change_vulnerability(False)

        self.__is_monsters_vulnerable = False

    # def item_ready_to_remove(self,item):
    #    self.__MAP.remove_item(item)
