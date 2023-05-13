from gui.Menu.Components.Scene import Scene

from ..Components.Image import Image
from ..Components.Scene import *
from ..Components.Button import *
from ..Components.TextArea import *


class GhostBonusScene(Scene):

    def __init__(self, screen, title, text, images_name):
        super().__init__(screen)

        self.rectangle_window = pygame.rect.Rect((100, 200), (514, 500))

        self.title = TextArea(Vector2d(285, 200), 314, 100, title, self.screen, rgb=(247, 245, 245),
                              font_size=30)

        self.content = TextArea(Vector2d(375, 150), 414, 200, text, self.screen, rgb=(247, 245, 245),
                                font_size=25, center_pos=False)

        self.images = [Image(Vector2d(500, 332), 50, 50, screen, path) for path in
                       images_name]

    def draw(self, mouse):
        pygame.draw.rect(self.screen, 'black', self.rectangle_window)

        self.title.draw()
        self.content.draw()
        self.images[self.sprite_nr % len(self.images)].draw()
