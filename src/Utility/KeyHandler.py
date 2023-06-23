import pygame


class KeyHandler:
    def __init__(self):
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.space_pressed = False

        # Settings
        self.UP = pygame.K_UP
        self.DOWN = pygame.K_DOWN
        self.LEFT = pygame.K_LEFT
        self.RIGHT = pygame.K_RIGHT
        self.SPACE = pygame.K_SPACE

    def key_pressed(self, e : pygame.event):
        if e.key == self.UP:
            self.up_pressed = True
        if e.key == self.DOWN:
            self.down_pressed = True
        if e.key == self.LEFT:
            self.left_pressed = True
        if e.key == self.RIGHT:
            self.right_pressed = True
        if e.key == self.SPACE:
            self.space_pressed = True

    def key_released(self,e: pygame.event):
        if e.key == pygame.K_w or e.key == self.UP:
            self.up_pressed = False
        if e.key == pygame.K_s or e.key == self.DOWN:
            self.down_pressed = False
        if e.key == pygame.K_a or e.key == self.LEFT:
            self.left_pressed = False
        if e.key == pygame.K_d or e.key == self.RIGHT:
            self.right_pressed = False
        if e.key == self.SPACE:
            self.space_pressed = False
    
