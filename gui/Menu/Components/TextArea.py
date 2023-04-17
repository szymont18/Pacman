import pygame


class TextArea:
    def __init__(self, pos: (int, int), width, height, txt: str, screen, fontname="comicsanms", font_size=80,
                 rgb=(196, 191, 37)):
        self.pos = pos #pos[0] - y; pos[1] - x
        self.txt = txt
        self.screen = screen
        self.rectangle = pygame.rect.Rect((pos[1], pos[0]), (width, height))
        self.fontname = fontname
        self.font_size = font_size
        self.rgb = rgb

    def draw(self):
        font = pygame.font.SysFont(self.fontname, self.font_size)
        text_surface = font.render(self.txt, True, self.rgb)
        text_rect = text_surface.get_rect(center=self.rectangle.center)
        pygame.draw.rect(self.screen, 'black', self.rectangle, 0, 5)
        self.screen.blit(text_surface, text_rect)





