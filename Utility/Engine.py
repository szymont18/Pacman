import random
import time
import pygame, sys
from Items.BonusLife import BonusLife
from Items.BonusMoney import BonusMoney
from Utility.CollisionChecker import *
from MapElements.Pacman import Pacman
from Items.Item import Item
from Items.Dot import Dot
from Items.Nuke import Nuke
from Items.RedBall import RedBall
from Items.Slow import Slow
from random import randint
from numpy.random import randint
from Enums.MonsterTypes import *
from MapElements.Skull import *
from MapElements.Demon import *
from MapElements.Ghost import *
from Utility.GameSpec import *
from Utility.KeyHandler import *
from MapElements.Pacman import *
from gui.Menu.Scenes.LevelStatusScene import STATUS, LevelStatusScene


class Engine(object):
    def __init__(self, MAP, MAX_ROW, MAX_COL, APP, KEYH, FIELD_SIZE, GAME_SPEC: GameSpec):
        # CONSTANTS
        self.TPS = 120  # tick rate
        self.STARTING_LIVES = 3 #Health at the begining of the game
        self.MAX_MONSTERS_ALIVE = -1  # When __enemies_alive == MAX_ENEMIES_ALIVE then monsters don't spawn
        self.MONSTER_APEAR_TIME = 5  # Every 5 seconds a new monster appears as long as the monster limit isn't exceeded
        self.GROW_TIME = 0.5  # Every 0.5 seconds the newborn map_element grows in size until it becomes an adult
        self.DIE_TIME = 0.2  # Every 0.2 seconds map_element death animation progresses
        self.BONUS_APEAR_TIME = 10  # Every 10 seconds a random bonus appears on the map
        self.BONUS_DISAPEAR_TIME = 5  # After 10 seconds if not picked up - bonus disappears
        self.CAN_EAT_SKULLS_DURATION = 5  # Pacman can eat skulls for 5 seconds from when he picks up a red orb
        self.ENEMIES_SLOWED_DURATION = 10 #Enemies are slowed for this amount of seconds after picking up slow down bonus
        self.BLINK_TIME = 5  # For 5 seconds, Pacman cannot be damaged (god mode)
        self.ITEM_BLINK_TIME = 0.2  # Every 0.2 seconds items blink
        self.EAT_TIME_FACE = 0.1  # How after does Pacman's mouth move
        self.MUSIC_BACKGROUND = None #Music to be played in the background


        # GAME
        self.__GAME_SPEC = GAME_SPEC #Aditional Games settings
        self.__lives = GAME_SPEC.get_lives() #Current lives
        self.__score = GAME_SPEC.get_score() #Current score
        self.__dots_eaten = 0 #Current dots consumed
        self.__can_eat_skulls = False
        self.__can_eat_skulls_remaining_time = -float('inf')
        self.__enemies_are_slow_remaining_time = -float('inf')
        self.__are_monsters_slowed = False

        self.__keep_running = True  # if engine still has to run
        self.__game_on = True  # If neither of sides won the game yet
        self.__game_won = False  # if pacman won
        self.__is_paused = False #Flag to pause the game
        self.__pacman = None  # handler to Pacman

        self.__monsters = dict()  # Dict to store monsters
        self.next_monster_id = 0  # New monsters receive unique monster ids
        self.__monsters_alive = 0
        self.__is_monsters_vulnerable = False # are_monsters_vulnerable*

        self.__tps_delta = 0.0
        self.__tps_clock = pygame.time.Clock()
        self.__APP = APP
        self.MAX_COL = MAX_COL
        self.MAX_ROW = MAX_ROW
        self.__MAP = MAP
        self.FIELD_SIZE = FIELD_SIZE
        self.__C_CHECKER = CollisionChecker(self, self.__MAP)  # Responsible for moving and lifting items
        self.spawn_pacman(KEYH)
        self.__KEYH = KEYH #Object responsible for handling keyboard buttons
        self.__difficulty = self.__GAME_SPEC.get_hardness()

        if self.__difficulty == HARDNESS.EASY:
            self.MAX_MONSTERS_ALIVE = 3
            print("Easy mode")
        elif self.__difficulty == HARDNESS.MEDIUM:
            self.MAX_MONSTERS_ALIVE = 4
            print("Medium mode")
        else:
            self.MAX_MONSTERS_ALIVE = 5
            print("Hard mode")



    def spawn_pacman(self, KEYH):
        spawn_x = self.__MAP.get_pacman_spawn_x()
        spawn_y = self.__MAP.get_pacman_spawn_y()
        self.__pacman = Pacman(spawn_x, spawn_y, self.FIELD_SIZE, KEYH, self.__C_CHECKER, self.__MAP, self,
                               self.GROW_TIME, self.DIE_TIME, self.BLINK_TIME, self.EAT_TIME_FACE, 5, 5)

    def spawn_monster(self, init_monster_type=None, init_pos_x=None, init_pos_y=None):
        monster = None

        # If a monster has been indicated and where it is to spawn, we do not draw a monster, we only place it once
        if init_monster_type is not None and init_pos_x is not None and init_pos_y is not None:
            if init_monster_type == MonsterTypes.SKULL:
                monster = Skull(init_pos_x, init_pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self,
                                self.next_monster_id, self.GROW_TIME, self.DIE_TIME, 4, 5)
            elif init_monster_type == MonsterTypes.DEMON:
                monster = Demon(init_pos_x, init_pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self,
                                self.next_monster_id, self.GROW_TIME, self.DIE_TIME, 4, 5)
            elif init_monster_type == MonsterTypes.GHOST:
                monster = Ghost(init_pos_x, init_pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self,
                                self.next_monster_id, self.GROW_TIME, self.DIE_TIME, 4, 5)
            else:
                raise("Wrong monster type")

        else:  # Random Monster
            monster_types = self.__MAP.POSSIBLE_MONSTERS
            n1 = len(monster_types)
            random_id = randint(0, n1)
            monster_type = monster_types[random_id]  # This monster

            spawn_tiles = self.__MAP.MONSTER_SPAWN_TILES
            n2 = len(spawn_tiles)
            random_id = randint(0, n2)
            spawn_tile = spawn_tiles[random_id]  # Coordinates

            pos_x = spawn_tile[0] * self.FIELD_SIZE
            pos_y = spawn_tile[1] * self.FIELD_SIZE

            if monster_type == MonsterTypes.SKULL:
                monster = Skull(pos_x, pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self, self.next_monster_id,
                                self.GROW_TIME, self.DIE_TIME, 4, 5)
            elif monster_type == MonsterTypes.DEMON:
                monster = Demon(pos_x, pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self, self.next_monster_id,
                                self.GROW_TIME, self.DIE_TIME, 4, 5)
            elif monster_type == MonsterTypes.GHOST:
                monster = Ghost(pos_x, pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self, self.next_monster_id,
                                self.GROW_TIME, self.DIE_TIME, 4, 5)

        self.__monsters[self.next_monster_id] = monster
        self.next_monster_id += 1
        self.__monsters_alive += 1

    #Method to kill monster and grant pacman adequate score (Moved to map_element_died) because it was only used there
    #def remove_monster(self, monster_id):
    #    self.__monsters[monster_id] = None
    #    self.__monsters_alive -= 1
    #    self.__score +=  1000 #Should depend on the type of monster

    #Few monsters are spawned at the beggining of the game
    def spawn_onload_monsters(self):
        monsters = self.__MAP.get_onload_monsters()
        for monster_type, (row, col) in monsters:
            self.spawn_monster(monster_type, col * self.FIELD_SIZE, row * self.FIELD_SIZE)

    # All things that should be set after pacman wins
    #This method initializes pacman win animation - it should not shut down the engine
    def pacman_won(self):
        win_sound = pygame.mixer.Sound('resources/Sound/LevelComplete.wav')
        win_sound.play()
        self.__pacman.win()  # will cause pacman to stop and play the joy of winning animation
        self.__game_on = False
        self.__game_won = True
        self.__pacman.set_visible(True)
        pygame.mixer.music.unload()

        #self.__MAP.clear_items() #No need to clear 'em
        self.__monsters = dict()
        self.__monsters_alive = 0

        print("Wygrales")
        print("Nacisnij spacje aby przejsc do nastepnego poziomu")
        #self.shut_down()

    #This method is called once pacman played his death animation - it should shut down engine on completion
    def pacman_lost(self):
        lose_sound = pygame.mixer.Sound('resources/Sound/GameOver.wav')
        lose_sound.play()
        self.__game_on = False
        self.__game_won = False
        self.__monsters_alive = 0
        pygame.mixer.music.unload()

        print("Przegrales")
        print("Nacisnij spacje aby kontynuowac")
        self.shut_down()

    #  Shut the main loop of the engine
    def shut_down(self):
        self.__keep_running = False

    #Start the level
    def run(self):
        #Music
        self.MUSIC_BACKGROUND = pygame.mixer.music.load(self.__MAP.get_music_path())
        pygame.mixer.music.play(-1)

        time_keeper = 0
        last_bonus_spawn_time = time.time()
        last_monster_spawn_time = time.time()

        self.spawn_onload_monsters()  # Spawn few monsters on the start

        while self.__keep_running:
            #EVENT SECTION
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


            # Until neither  of sides won
            if self.__game_on:
                # Moving map elements
                while self.__tps_delta > 1 / self.TPS:
                    self.update()
                    self.__tps_delta -= 1 / self.TPS

                #if self.__dots_eaten == 5:
                #    self.update()
                #    self.pacman_won()

                if self.__dots_eaten == self.__MAP.get_total_dots():
                    #self.update() #Moze te update wywalic nad ify
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

                pygame_time = pygame.time.get_ticks()
                if (self.__are_monsters_slowed and pygame_time - self.__enemies_are_slow_remaining_time > self.ENEMIES_SLOWED_DURATION * 1000):
                    self.return_normal_speed_to_enemies()

            else:  # if somebody wins (demons or pacman)
                self.update()
                if self.__pacman.get_played_epilog_animation():
                    self.shut_down()

            # Drawing
            self.draw()
            pygame.display.flip()

        # Save specification
        self.__GAME_SPEC.set_score(self.__score)
        self.__GAME_SPEC.set_lives(self.__lives)

        # End game - win / lose
        if self.__game_won:  # Win
            return STATUS.LVL_WIN
        elif not self.__game_on:  # Lose
            return STATUS.LVL_LOSE

        return 0  # Other (User left the game?)

    def update(self):
        self.__pacman.update()
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


    # We tell the engine to assign the bonuses associated with picking up the item and the item itself will inform
    # about picking it up (Item will play pick up animations)
    def picked_up(self, item: Item):
        pop_sound = pygame.mixer.Sound(item.get_sound_path())
        pop_sound.play()
        if isinstance(item, Dot):
            self.__dots_eaten += 1
            self.__score += 100

        elif isinstance(item, RedBall):
            self.__score += 200
            self.make_skulls_vulnerable()
        elif isinstance(item, BonusLife):
            self.__lives += 1
        elif isinstance(item, BonusMoney):
            self.__score += 10_000
        elif isinstance(item,Slow):
            self.slow_down_enemies()
        elif isinstance(item,Nuke):
            self.kill_all_enemies()

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


    # The method works a bit like notification of the observer after the death of a mob -
    # it is used to clean up after it
    #Method is called by MapElements when they bleed out (finish death animation) and they notify engine to remove them
    def map_element_died(self, element: MapElement):
        if isinstance(element, Pacman):  # Pacman die
            self.__lives = 0  # It's going to zero (???) TODO : Test if nessesary
            self.pacman_lost()

        else:  # We know it is a skull because its the only one pacman can kill (withot nuke bonus)
            self.__monsters[element.MONSTER_ID] = None
            self.__monsters_alive -= 1

    # A method used by enemies when they hit pacman to hurt or kill him
    def hurt_pacman(self):
        if not self.__pacman.is_hurt():
            self.__pacman.set_hurt(True)
            self.__lives -= 1
            pain_sound = pygame.mixer.Sound('resources/Sound/Death.wav')
            pain_sound.play()

        if self.__lives == 0:
            self.__pacman.kill()

    #Method called by Skull when it meets pacman, but its in mice form (vulnerable to pacman)
    def kill_Skull(self,skull):
        skull.kill() #Initializes skull bleedout, once skull bleeds out it calls map_element_died to notify engine
        pain_sound = pygame.mixer.Sound('resources/Sound/Victim.wav')
        pain_sound.play() #Play the sound of skull being killed
        self.__score += 1000 #Grant player adequate score


    def get_pacman_solid_area(self):
        return self.__pacman.SOLID_AREA

    def get_pacman_pos(self):
        return self.__pacman.get_pos_x(), self.__pacman.get_pos_y()

    #Pacman is in godmode for a few seconds once he is hurt
    def is_pacman_hurt(self):
        return self.__pacman.is_hurt()


    #Transforms Skulls into mice
    def make_skulls_vulnerable(self):
        for monster_id in self.__monsters:
            monster = self.__monsters[monster_id]
            if isinstance(monster, Skull) and monster.get_is_alive() and not monster.get_is_newborn():
                self.__monsters[monster_id].change_vulnerability(True)

        self.__can_eat_skulls_remaining_time = pygame.time.get_ticks()
        self.__is_monsters_vulnerable = True

    #Transforms mice back to skull form
    def make_skulls_predators(self):
        for monster_id in self.__monsters:
            monster = self.__monsters[monster_id]
            if isinstance(monster, Skull) and monster.get_is_alive() and not monster.get_is_newborn():
                self.__monsters[monster_id].change_vulnerability(False)

        self.__is_monsters_vulnerable = False

    def slow_down_enemies(self):
        for monster_id in self.__monsters:
            monster = self.__monsters[monster_id]
            if monster.get_is_alive() and not monster.get_is_newborn() and not isinstance(monster,Ghost):
                self.__monsters[monster_id].set_speed(2)
            elif monster.get_is_alive() and not monster.get_is_newborn(): #=> is a ghost
                self.__monsters[monster_id].set_speed(1)

        self.__enemies_are_slow_remaining_time = pygame.time.get_ticks()
        self.__are_monsters_slowed = True

    def return_normal_speed_to_enemies(self):
        for monster_id in self.__monsters:
            monster = self.__monsters[monster_id]
            if monster.get_is_alive() and not monster.get_is_newborn():
                self.__monsters[monster_id].set_speed(monster.MAX_SPEED)

        self.__are_monsters_slowed = False

    def kill_all_enemies(self):
        for monster_id in self.__monsters:
            monster = self.__monsters[monster_id]
            monster.kill()
            if isinstance(monster,Skull):
                self.__score += 1000
            elif isinstance(monster,Demon):
                self.__score += 5000
            elif isinstance(monster, Ghost):
                self.__score += 10000


