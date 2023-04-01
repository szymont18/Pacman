import pygame
from Button import *
from App import *

class Menu:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height

        # Rectangles button
        self.start_game_button = None
        self.create_level_button = None
        self.leader_board_button = None
        self.setting = None
        self.exit = None

        # Screen
        self.screen = screen

        # Background
        self.background_image = pygame.transform.scale(pygame.image.load('Level01.bmp'), (self.width, self.height))

    def draw(self):
        pygame.draw.rect(self.screen, 'black', [0, 0, self.width, self.height])
        self.screen.blit(self.background_image, (0, 0))

        self.start_game_button.draw()
        self.create_level_button.draw()
        self.leader_board_button.draw()
        self.setting.draw()
        self.exit.draw()

        self.start_game_button.is_clicked()
        self.create_level_button.is_clicked()
        self.leader_board_button.is_clicked()
        self.setting.is_clicked()
        self.exit.is_clicked()

    def set_buttons(self, start_game_button, create_level_button, leader_board_button,
                    setting, exit_button):
        self.start_game_button = start_game_button
        self.create_level_button = create_level_button
        self.leader_board_button = leader_board_button
        self.setting = setting
        self.exit = exit_button


def launch():
    App()

pygame.init()
screen = pygame.display.set_mode([816, 816])
start_button = Button((216, 388), "Start Game", screen, launch)
create_level = Button((276, 388), "Create Level", screen, lambda : print("Button 2"))
leader_board = Button((336, 388), "Leader_board", screen, lambda : print("Button 3"))
settings = Button((396, 388), "Settings", screen, lambda : print("Button 4"))
exit_button = Button((456, 388), "Exit_button", screen, lambda : print("Button 5"))

menu = Menu(816, 816, screen)
menu.set_buttons(start_button,create_level,leader_board,settings,exit_button)
fps = 60
timer = pygame.time.Clock()

run = True
while run:
    timer.tick(fps)
    menu.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()







