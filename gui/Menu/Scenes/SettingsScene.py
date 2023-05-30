from ..Components.Scene import *
from ..Components.Button import *
from ..Components.ScrollBar import *
from ..Components.TextArea import *
import pygame


class SettingsScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        self.rectangle_window = pygame.rect.Rect((100, 200), (514, 500))
        self.title = TextArea(Vector2d(200, 200), 314, 100, "Settings", self.screen, rgb=(247, 245, 245))

        self.sound_text = TextArea(Vector2d(285, 200), 314, 100, "Sound", self.screen, rgb=(247, 245, 245),
                                   font_size=30)
        self.sound_scroll_bar = ScrollBar(Vector2d(350, 200), 314, 25, self.screen, SettingsScene.change_sound)

        self.brightness_text = TextArea(Vector2d(375, 200), 314, 100, "Video", self.screen, rgb=(247, 245, 245),
                                        font_size=30)
        self.brightness_scroll_bar = ScrollBar(Vector2d(440, 200), 314, 25, self.screen,
                                               SettingsScene.change_brightness)

        self.game_speed_text = TextArea(Vector2d(465, 200), 314, 100, "Difficulty", self.screen, rgb=(247, 245, 245),
                                        font_size=30)
        self.game_speed_scroll_bar = ScrollBar(Vector2d(530, 200), 314, 25, self.screen,
                                               SettingsScene.change_hardness_rate)

        self.return_button = Button(Vector2d(600, 200), 314, 50, "Return", screen,
                                    lambda: Scene.change_menu_scene(SceneTypes.MAIN))

        # To delete soon
        pygame.mixer.music.load("resources/sound/test_sound.mp3")

    def draw(self, mouse):
        pygame.draw.rect(self.screen, 'black', self.rectangle_window)
        self.title.draw()
        self.sound_text.draw()
        self.return_button.draw()
        self.sound_scroll_bar.draw()
        self.brightness_text.draw()
        self.brightness_scroll_bar.draw()
        self.game_speed_text.draw()
        self.game_speed_scroll_bar.draw()

        self.sound_scroll_bar.is_clicked(mouse)
        self.brightness_scroll_bar.is_clicked(mouse)
        self.game_speed_scroll_bar.is_clicked(mouse)
        self.return_button.is_clicked(mouse)

    @staticmethod
    def change_sound(scroll_percentage):
        pygame.mixer.music.set_volume(scroll_percentage)
        pygame.mixer.music.play()

    @staticmethod
    def change_brightness(scroll_percentage):
        pygame.display.set_gamma(scroll_percentage)

    @staticmethod
    def change_hardness_rate(scroll_percentage):
        Scene.GAME_SPEC.set_hardness_ratio(scroll_percentage)
