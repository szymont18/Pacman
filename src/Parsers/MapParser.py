from ..Enums.MonsterTypes import MonsterTypes
from ..Enums.TileType import TileType
from ..Items.BonusLife import BonusLife
from ..Items.BonusMoney import BonusMoney
from ..Items.Nuke import Nuke
from ..Items.Slow import Slow
from ..MapElements.Skull import Skull
from ..Maps.Tile import Tile


class MapParser:
    def __init__(self, pathname):
        file = open(pathname)
        lines = file.readlines()

        first_line = lines[0]
        first_line = first_line.split()

        self.MAX_ROW = int(first_line[0])
        self.MAX_COL = int(first_line[1])
        self.FIELD_SIZE = 42
        self.TILES = self.get_map(lines[1:self.MAX_ROW + 1])
        self.PACMAN_START = eval(lines[self.MAX_ROW + 1])

        self.DOTS = []
        self.RED_DOTS = []
        self.BONUS_PROBABILITY = {}
        self.ONLOAD_MONSTERS = []
        self.POSSIBLE_MONSTERS = []
        self.MONSTER_TILES = []
        actual_row = self.MAX_ROW + 2
        if actual_row < len(lines):
            self.DOTS = [eval(tpl) for tpl in lines[actual_row].split(";")[:-1]]
        actual_row += 1
        if actual_row < len(lines):
            self.RED_DOTS = [eval(tpl) for tpl in lines[actual_row].split(";")[:-1]]
        actual_row += 1
        if actual_row < len(lines):
            self.BONUS_PROBABILITY = self.get_bonus(lines[actual_row])
        actual_row += 1
        if actual_row < len(lines):
            self.ONLOAD_MONSTERS, self.POSSIBLE_MONSTERS = self.get_on_load_monsters(lines[actual_row])
        actual_row += 1
        if actual_row < len(lines):
            self.MONSTER_TILES = self.get_monster_tiles(lines[actual_row])
        file.close()

    def get_map(self, str_map):
        def create_tile(x):
            print(x)
            x = int(x)
            return Tile(TileType(x))

        pacman_map = []
        for line in str_map:
            pacman_map.append(list(map(create_tile, line[:-1].split())))
        return pacman_map

    def get_bonus(self, str_bonus):
        bonus_probability = {}
        for bns in str_bonus.split(";")[:-1]:
            bonus_name, prob, plc = eval(bns)
            # prob = int(prob)
            # row = int(row)
            # col = int(col)

            if bonus_name == "BonusLife":
                bonus_name = BonusLife
            elif bonus_name == "BonusMoney":
                bonus_name = BonusMoney
            elif bonus_name == "Slow":
                bonus_name = Slow
            elif bonus_name == "Nuke":
                bonus_name = Nuke

            bonus_probability[bonus_name] = (prob, plc)

        return bonus_probability

    def get_on_load_monsters(self, monster_line):
        on_load_monster = []
        possible_monsters = [MonsterTypes.SKULL]
        for monster_spec in monster_line.split(";")[:-1]:
            monster_type, row, col = eval(monster_spec)
            monster_type = MonsterTypes(monster_type)

            on_load_monster.append((monster_type, (row, col)))

        return on_load_monster, possible_monsters

    def get_monster_tiles(self, monster_tiles_line):
        tiles = []
        for monster_spec in monster_tiles_line.split(";")[:-1]:
            tpl = eval(monster_spec)
            tiles.append((tpl[1], tpl[0]))
        return tiles

    def get_all_params(self):
        return (
        self.MAX_ROW, self.MAX_COL, self.FIELD_SIZE, self.PACMAN_START[1], self.PACMAN_START[0], self.POSSIBLE_MONSTERS,
        self.MONSTER_TILES, self.ONLOAD_MONSTERS, self.RED_DOTS, self.TILES, self.DOTS, self.BONUS_PROBABILITY)
