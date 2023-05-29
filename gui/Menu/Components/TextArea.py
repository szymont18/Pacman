import pygame
import pygame.freetype
from MapElements.Vector2d import Vector2d


class TextArea:
    def __init__(self, pos: Vector2d, width, height, txt: str, screen, fontname="comicsanms", font_size=80,
                 rgb=(196, 191, 37), center_pos=True, bck_rgb = 'black'):
        self.pos = pos
        self.txt = txt
        self.width = width
        self.height = height

        self.screen = screen
        self.rectangle = pygame.rect.Rect(self.pos.get_coords(), (width, height))
        self.center_pos = center_pos

        self.font_size = font_size
        self.font = pygame.font.SysFont(fontname, font_size)

        self.rgb = rgb
        self.bck_rgb = bck_rgb

    def draw(self):
        # text_surface = self.font.render(self.txt, True, self.rgb)
        # text_rect = text_surface.get_rect(center=self.rectangle.center)
        pygame.draw.rect(self.screen, self.bck_rgb, self.rectangle, 0, 5)

        # self.screen.blit(text_surface, text_rect)
        if self.center_pos:
            TextArea.renderTextCenteredAt(self.txt, self.font, self.rgb, self.rectangle.centerx,
                                          self.rectangle.centery - (self.font_size / 2), self.screen, self.width)
        else:
            TextArea.renderTextCenteredAt(self.txt, self.font, self.rgb, self.rectangle.centerx,
                                          self.pos.get_y(), self.screen, self.width)

    @staticmethod
    def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
        # first, split the text into words
        words = text.split()

        # now, construct lines out of these words
        lines = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = font.size(' '.join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            # add a line consisting of those words
            line = ' '.join(line_words)
            lines.append(line)

        # now we've split our text into lines that fit into the width, actually
        # render them

        # we'll render each line below the last, so we need to keep track of
        # the culmative height of the lines we've rendered so far
        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            # (tx, ty) is the top-left of the font surface
            tx = x - fw / 2
            ty = y + y_offset

            font_surface = font.render(line, True, colour)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh
