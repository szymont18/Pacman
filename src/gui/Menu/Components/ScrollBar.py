import pygame

from src.MapElements.Vector2d import Vector2d


class ScrollBar:
    def __init__(self, pos: Vector2d, width: int, height: int, screen, action, scroll_rgb=(100, 100, 100),
                 bar_rgb=(255, 255, 255)):

        self.pos = pos
        self.scroll_x = pos.get_x()
        self.width = width
        self.height = height

        self.screen = screen

        self.scroll_rgb = scroll_rgb
        self.bar_rgb = bar_rgb

        self.action = action

    def draw(self):
        pygame.draw.rect(self.screen, self.bar_rgb, ((self.pos.get_coords()), (self.width, self.height)))

        scroll_position = max(self.scroll_x, self.pos.get_x())
        scroll_position = min(scroll_position, self.scroll_x + self.width)
        pygame.draw.rect(self.screen, self.scroll_rgb, (scroll_position, self.pos.get_y(), 10, self.height))

    def is_clicked(self, event):
        if event is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if self.pos.get_y() < mouse_y < self.pos.get_y() + self.height and \
                    self.pos.get_x() < mouse_x < self.pos.get_x() + self.width:

                self.scroll_change_action(mouse_x)

    def scroll_change_action(self, new_pos):
        scroll_percentage = (new_pos - self.pos.get_x()) / self.width

        print(scroll_percentage)
        self.action(scroll_percentage)
        self.scroll_x = new_pos







