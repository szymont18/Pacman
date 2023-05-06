import pygame

from MapElements.Vector2d import Vector2d


class Image:
    def __init__(self, pos: Vector2d, width, height, screen, pathname):
        self.pos = pos
        self.width = width
        self.height = height

        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(pathname), (width, height))

    def draw(self):
        self.screen.blit(self.image, self.pos.get_coords())

