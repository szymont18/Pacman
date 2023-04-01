import pygame


class Button:
    def __init__(self, pos: (int, int), text: str, screen, action=None, color='blue3'):
        self.pos = pos
        self.text = text
        self.button = pygame.rect.Rect((pos[1], pos[0]), (260, 40))

        # Set action to each button
        self.action = action
        self.screen = screen
        self.color = color

    def draw(self):
        pygame.draw.rect(self.screen, 'light gray', self.button, 0, 5)
        font = pygame.font.Font('freesansbold.ttf', 24)
        text2 = font.render(self.text, True, 'black')
        self.screen.blit(text2, (self.pos[1] + 15, self.pos[0] + 7))

    def is_clicked(self):
        if pygame.mouse.get_pressed()[0] and self.button.collidepoint(pygame.mouse.get_pos()):
            return self.action


