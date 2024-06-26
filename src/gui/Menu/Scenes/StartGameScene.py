from enum import Enum

from src.Enums.SceneTypes import SceneTypes
from src.MapElements.Vector2d import Vector2d
from ..Components.Image import Image
from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *
import os


class MAPTYPE(Enum):
    CHOSE = 0
    ORIGINAL = 1
    CASUAL = 2


class StartGameScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        self.rectangle_window = pygame.rect.Rect((100, 200), (514, 500))
        self.title = TextArea(Vector2d(200, 150), 414, 100, "Chose map", self.screen, rgb=(247, 245, 245))
        self.text1 = "By clicking on the maps below, you will start the game. Maps marked with a padlock are not " \
                     "available. You can also choose one of the previously created maps, which you will find by " \
                     "clicking the My Maps button. To be able to qualify for the leaderboard, you must start the game " \
                     "from level one. GOOD LUCK!"

        self.map_type = MAPTYPE.CHOSE

        self.exp_text = TextArea(Vector2d(300, 150), 414, 150, self.text1, self.screen, rgb=(247, 245, 245),
                                 font_size=25, center_pos=False)

        self.original_maps = Button(Vector2d(495, 150), 150, 50, "Original Maps", self.screen,
                                    lambda: self.change_map_type(MAPTYPE.ORIGINAL))

        self.casual_maps = Button(Vector2d(495, 414), 150, 50, "Casual Maps", self.screen,
                                  lambda: self.change_map_type(MAPTYPE.CASUAL))

        self.return_button = Button(Vector2d(600, 200), 314, 50, "Return", screen,
                                    lambda: Scene.change_menu_scene(SceneTypes.MAIN))

        self.return_to_chose_button = Button(Vector2d(600, 200), 314, 50, "Return", screen,
                                             lambda: self.change_map_type(MAPTYPE.CHOSE))

        self.offset = 0
        self.original_maps_images = [Image(Vector2d(350, 116 + (i % 3) * 150 + (i % 3) * 16), 150, 150, self.screen,
                                           f'resources/maps/Level{i + 1}.png') for i in range(0, 15)]

        self.original_maps_start_buttons = [Button(Vector2d(350, 116 + (i % 3) * 150 + (i % 3) * 16), 150, 150, f'{i}',
                                                   self.screen) for i in range(0, 18)]

        self.prev_image = Image(Vector2d(525, 200), 100, 50, self.screen, f'resources/menu/left.png')
        self.next_image = Image(Vector2d(525, 414), 100, 50, self.screen, f'resources/menu/right.png')
        self.prev_button = Button(Vector2d(525, 200), 100, 50, "", self.screen,
                                  lambda: self.change_offset(self.offset - 1))
        self.next_button = Button(Vector2d(525, 414), 100, 50, "", self.screen,
                                  lambda: self.change_offset(self.offset + 1))
        # self.prev_button = Button(Vector2d(550, 200), 100)

        #     TODO: AFTER MAP CREATOR MODIFY THIS

        self.casual_maps_images = [TextArea(Vector2d(350, 116 + (i % 3) * 150 + (i % 3) * 16), 150, 150, file_name[:-4],
                                            self.screen, rgb=(247, 245, 245),bck_rgb='red', font_size=40) for i, file_name in
                                   enumerate(os.listdir("resources/usermaps/"))]


    def draw(self, mouse):
        pygame.draw.rect(self.screen, 'black', self.rectangle_window)
        self.title.draw()
        if self.map_type == MAPTYPE.CHOSE:
            self.exp_text.draw()
            self.return_button.draw()
            self.original_maps.draw()
            self.casual_maps.draw()

            self.casual_maps.is_clicked(mouse)
            self.original_maps.is_clicked(mouse)
            self.return_button.is_clicked(mouse)

        elif self.map_type == MAPTYPE.ORIGINAL:
            self.return_to_chose_button.draw()
            self.draw_maps(mouse)
            self.prev_button.draw()
            self.next_button.draw()
            self.prev_image.draw()
            self.next_image.draw()

            self.prev_button.is_clicked(mouse)
            self.next_button.is_clicked(mouse)
            self.return_to_chose_button.is_clicked(mouse)

        else:
            self.return_to_chose_button.draw()
            self.draw_maps(mouse)
            self.prev_button.draw()
            self.next_button.draw()
            self.prev_image.draw()
            self.next_image.draw()

            self.prev_button.is_clicked(mouse)
            self.next_button.is_clicked(mouse)
            self.return_to_chose_button.is_clicked(mouse)

    def change_map_type(self, new_type):
        self.map_type = new_type
        if new_type == MAPTYPE.CASUAL:
            self.casual_maps_images = [
                TextArea(Vector2d(350, 116 + (i % 3) * 150 + (i % 3) * 16), 150, 150, file_name[:-4],
                         self.screen, rgb=(247, 245, 245), bck_rgb='red', font_size=40) for i, file_name in
                enumerate(os.listdir("resources/usermaps/"))]

        self.offset = 0

    # TODO CHANGE 10 TO PARAMS
    def change_offset(self, new_offset):
        if new_offset < 0 or new_offset >= 10: return
        self.offset = new_offset

    def launch_game(self, game_id):
        if self.map_type == MAPTYPE.ORIGINAL:
            print(f'Start game {game_id}')
            Scene.GAME_SPEC.set_start_level(game_id)
        else:
            print(f'Start game {game_id}')
            Scene.GAME_SPEC.set_pathname("resources/usermaps/"+game_id+".txt")

    def draw_maps(self, mouse):
        image_to_draw = []
        buttons_to_click = []
        if self.map_type == MAPTYPE.ORIGINAL:
            image_to_draw = self.original_maps_images
            buttons_to_click = self.original_maps_start_buttons

        elif self.map_type == MAPTYPE.CASUAL:
            image_to_draw = self.casual_maps_images
            buttons_to_click = self.original_maps_start_buttons
        else:
            return

        act1, act2, act3 = self.offset * 3, self.offset * 3 + 1, self.offset * 3 + 2
        for i in range(self.offset * 3, self.offset * 3 + 3):
            if i >= len(image_to_draw): continue
            # print(i)
            image_to_draw[i].draw()
            if self.map_type == MAPTYPE.ORIGINAL:
                buttons_to_click[i].set_action(lambda: self.launch_game(act1))
            else:
                buttons_to_click[i].set_action(lambda: self. launch_game(image_to_draw[i].txt))
            buttons_to_click[i].is_clicked(mouse)
            act1, act2 = act2, act3
