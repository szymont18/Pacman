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
from numpy.random import randint
from Enums.MonsterTypes import *
from MapElements.Skull import *
from MapElements.Demon import *
from Utility.KeyHandler import *
from MapElements.Pacman import *

class Engine(object):
    def __init__(self,MAP,MAX_ROW,MAX_COL,APP,KEYH,FIELD_SIZE):
        pygame.init()

        #STALE
        self.TPS = 120 #tickrate
        self.STARTING_LIVES = 3
        self.MAX_MONSTERS_ALIVE = 4 # Gdy __enemies_alive == MAX_ENEMIES_ALIVE to potwory sie nie respia
        self.MONSTER_APEAR_TIME = 5 #Co 5 sekund  pojawia sie nowy potwor o ile limit potworow nie przekroczony
        self.GROW_TIME = 0.5  #Co 0.5 sekundy nowonarodzony map_element sie powieksza az staje sie dorosly po 5 zwiekszeniach (dot. pacmana i potworkow)
        self.BONUS_APEAR_TIME = 10 # Co 10 sekund pojawia sie na mapie losowy bonus
        self.BONUS_DISAPEAR_TIME = 1200 # Po 10 sekundach jesli nie podniesiony - znika
        self.__tps_delta = 0.0
        self.__tps_clock = pygame.time.Clock()

        #Rozgrywka
        self.__lives = 3
        self.__score = 0
        self.__dots_eaten = 0

        self.__keep_running = True # czy silnik ma dalej pracowac
        self.__game_on = True #Czy rozgrywka ciagle trwa czy moze jedna ze stron juz wygrala
        self.__is_paused = False
        self.__pacman = None # uchwyt do pacmana

        self.__monsters = dict()  # Dict do przechowywania potworow
        self.next_monster_id = 0 #id nastepnego respionego potworka
        self.__monsters_alive = 0

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
        self.__pacman = Pacman(spawn_x, spawn_y, self.FIELD_SIZE, KEYH, self.__C_CHECKER, self.__MAP, self,self.GROW_TIME)


    def spawn_monster(self, init_monster_type=None, init_pos_x=None, init_pos_y=None):
        monster = None

        #Jesli wskazano jaki potwor i gdzie ma sie zrespic to nie losujemy potwora tylko od razy go kladziemy
        if init_monster_type != None and init_pos_x != None and init_pos_y != None:
            #print("juz predefined")
            if init_monster_type == MonsterTypes.SKULL:
                monster = Skull(init_pos_x, init_pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self, self.next_monster_id,self.GROW_TIME)
            elif init_monster_type == MonsterTypes.DEMON:
                monster = Demon(init_pos_x, init_pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self, self.next_monster_id,self.GROW_TIME)

        else: #Potwor bedzie losowany
            monster_types = self.__MAP.POSSIBLE_MONSTERS
            n1 = len(monster_types)
            random = randint(0, n1)
            monster_type = monster_types[random]  # ten potworek ma sie zrespic

            #print("spawn_monster")
            #print(monster_type)

            spawn_tiles = self.__MAP.MONSTER_SPAWN_TILES
            n2 = len(spawn_tiles)
            random = randint(0, n2)
            spawn_tile = spawn_tiles[random]  # na tym polu ma sie zrespic potworek

            #monster = None
            pos_x = spawn_tile[0] * self.FIELD_SIZE
            pos_y = spawn_tile[1] * self.FIELD_SIZE

            if monster_type == MonsterTypes.SKULL:
                monster = Skull(pos_x, pos_y, self.FIELD_SIZE, self.__C_CHECKER, self.__MAP, self, self.next_monster_id,self.GROW_TIME)

        self.__monsters[self.next_monster_id] = monster
        #print(self.__MONSTERS[self.next_monster_id])
        self.next_monster_id+=1
        self.__monsters_alive +=1

    def remove_monster(self,monster_id):
        self.__monsters.pop(monster_id)
        self.__monsters_alive -=1
        print("usunieto")

    def spawn_onload_monsters(self):
        #print("spawning onload monsters")
        monsters = self.__MAP.get_onload_monsters()

        for monster_type , (row,col) in monsters:
            self.spawn_monster(monster_type,col*self.FIELD_SIZE,row*self.FIELD_SIZE)

    #Metoda konczy gre zwycieztwem pacmana
    def pacman_won(self):
        #self.__pacman.set_speed(0)
        self.__pacman.win() #metoda sprawi ze pacman sie zatrzyma i odtworzy animacje radosci z wygranej
        self.__game_on = False


        self.__monsters = dict()
        self.__monsters_alive = 0

        print("Wygrales")
        print("Nacisnij spacje aby przejsc do nastepnego poziomu")

    #Zgaszenie glownej petli silnika - koniec programu
    def shut_down(self):
        self.__keep_running = False

    def run(self):

        #time_keeper, last_time = 0, time.time()

        time_keeper = 0
        last_bonus_spawn_time = time.time()
        last_monster_spawn_time = time.time()

        self.spawn_onload_monsters() #Funkcja respi kilka potworkow na start

        while self.__keep_running:
            #print(self.__MAP.get_total_dots())
            #SEKCJA EVENTOW
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

            #SEKCJA PORUSZANIA ELEMENTOW MAPY
            while self.__tps_delta > 1 / self.TPS:
                self.update()
                self.__tps_delta -= 1 / self.TPS


            #Metody w tym bloku maja sie wykonywac jedynie gdy zadna ze stron jeszcze nie wygrala
            if self.__game_on:
                # METODA NA CZAS TESTOWANIA
                #if self.__dots_eaten == 5:
                #    self.pacman_won()

                if self.__dots_eaten == self.__MAP.get_total_dots():
                    self.pacman_won()


                # SEKCJA RESPIENIA POTWOROW I ITEMOW
                time_keeper = time.time()
                if time_keeper - last_bonus_spawn_time > self.BONUS_APEAR_TIME:
                    last_bonus_spawn_time = time.time()
                    self.spawn_bonus()

                if time_keeper - last_monster_spawn_time > self.MONSTER_APEAR_TIME and self.__monsters_alive < self.MAX_MONSTERS_ALIVE:
                    last_monster_spawn_time = time.time()
                    self.spawn_monster()
            else: #Metody z tego bloku maja sie wywolac jedynie gdy jedna ze stron wygrala

                if self.__KEYH.space_pressed: self.__keep_running = False



            #SEKCJA RYSOWANIA
            self.draw()
            pygame.display.flip()

        #W tym momencie gry sie skonczyla (wygralismy lub przegralismy)
        if self.__dots_eaten == self.__MAP.get_total_dots() or self.__dots_eaten == 5:  # Pacman wygral
            return 10
        elif self.__lives == 0: #Pacman zmarl
            return -10

        return 0

    def update(self):
        self.__pacman.update()
        #Ruszenie potworkow
        for monster_id in self.__monsters.keys():
            #print("potwor bedzie ruszany")
            self.__monsters[monster_id].update()


    def draw(self):
        self.__APP.clear_map() #czysci ekran
        self.__APP.draw_map(self.__MAP)
        self.__APP.draw_items(self.__MAP)

        self.__APP.draw_map_element(self.__pacman)
        for monster_id in self.__monsters.keys():
            self.__APP.draw_map_element(self.__monsters[monster_id])

        self.__APP.draw_pacman_status(self.__lives, self.__score)



    def picked_up(self, item: Item):
        if isinstance(item, Dot):
            self.__dots_eaten += 1
            #print(f"Ate {self.__dots_eaten} dots")

            #print()
            #for item in self.__MAP._items:
            #    print(item)

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

    #Metoda dziala troche jak notyfikacja obserwera po smierci moba - sluzy do sprzatniecia po nim
    def map_element_died(self,element : MapElement):
        if isinstance(element,Pacman): #Pacman zginal
            self.__lives = 0 #Narazie na zero zeby przetestowac giniecie pacmana
            self.__keep_running = False
        else: #Wiemy ze to potwor
            self.remove_monster(element.MONSTER_ID)

    #Metoda sluzy o zabicia moba, ktory odegra animacja smierci a nastepnie zawola metode map_element_died informujac silnik ze mozna go usunac z mapy
    def kill_map_element(self,element):
        element.kill()

    #Metoda wolana przez duchy ktory wejda na pacmana, ale nie maja dostepu do wskaznika na pacmana wiec nie zawolaja bezposrednio metody kill()
    def kill_pacman(self):
        print("pacman zabijany")
        self.kill_map_element(self.__pacman)

    def get_pacman_solid_area(self):
        #print("printuje")
        #print(self.__pacman.SOLID_AREA)
        return self.__pacman.SOLID_AREA

    def get_pacman_pos(self):
        return self.__pacman.get_pos_x(), self.__pacman.get_pos_y()


