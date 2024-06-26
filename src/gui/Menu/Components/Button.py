import pygame

from src.MapElements.Vector2d import Vector2d


class Button:
    REACTION_TIME = -float('inf')
    def __init__(self, pos: Vector2d, width, height, text: str, screen, action=None,  fontname="comicsanms",
                 font_size=30, rgb=(247, 245, 245)):
        self.pos = pos
        self.text = text
        self.button = pygame.rect.Rect(pos.get_coords(), (width, height))

        # Set action to each button
        self.action = action
        self.screen = screen

        # Details
        self.fontname = fontname
        self.font_size = font_size
        self.font_rgb = rgb
        self.button_color = 'black'

        self.actual_font_rgb = rgb
        self.on_click_font_rgb = (196, 191, 37)

        self.actual_button_color = self.button_color
        self.on_click_button_rgb = (117, 110, 110)

    def draw(self):
        font = pygame.font.SysFont(self.fontname, self.font_size)
        text_surface = font.render(self.text, True, self.actual_font_rgb)
        text_rect = text_surface.get_rect(center=self.button.center)
        pygame.draw.rect(self.screen, self.actual_button_color, self.button, 0, 5)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, event):

        if event is not None and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION):
            if self.button.collidepoint(event.pos):
                self.actual_font_rgb = self.on_click_font_rgb
                self.actual_button_color = self.on_click_button_rgb
            else:
                self.actual_button_color = self.button_color
                self.actual_font_rgb = self.font_rgb

        if pygame.mouse.get_pressed()[0] and self.button.collidepoint(pygame.mouse.get_pos()):
            if pygame.time.get_ticks() - Button.REACTION_TIME < 500: return

            Button.REACTION_TIME = pygame.time.get_ticks()
            self.action()

    def change_cover_colors(self, new_text_color, new_rectangle_color):
        self.on_click_button_rgb = new_rectangle_color
        self.on_click_font_rgb = new_text_color


    def set_action(self, action):
        self.action = action