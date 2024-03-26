
import pygame

from src.MapElements.Vector2d import Vector2d
from src.gui.Menu.Components.Scene import Scene


class TextInput:
    def __init__(self, pos: Vector2d, width: int, height: int, screen, fontname="comicsanms", font_size=45,
                 text_rgb=(247, 245, 245), rect_active_rgb=(196, 191, 37), rect_nonactive_rgb=(247, 245, 245)):

        self.pos = pos
        self.rect = pygame.Rect(pos.get_x(), pos.get_y(), width, height)
        self.height = height
        self.width = width
        self.screen = screen

        self.text = ""

        self.font = pygame.font.SysFont(fontname, font_size) # Changed

        self.text_rgb = text_rgb

        self.rect_rgb = rect_nonactive_rgb
        self.active_rgb = rect_active_rgb
        self.non_active_rgb = rect_nonactive_rgb

        self.txt_surface = self.font.render(self.text, True, self.text_rgb)

        self.active = False

    def is_clicked(self, event):
        if event is None: return

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.rect_rgb = self.active_rgb if self.active else self.non_active_rgb

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_SPACE:
                    file = open("resources/leader_board.csv", "a")
                    text2save = f'{self.text},{Scene.GAME_SPEC.get_score()},{Scene.GAME_SPEC.get_str_time()}\n'
                    file.write(text2save)
                    file.close()
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.rect_rgb)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(self.screen, self.rect_rgb, self.rect, 2)

