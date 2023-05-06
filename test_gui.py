import pygame

from gui.Menu.Menu import Menu

pygame.init()
screen = pygame.display.set_mode([714, 798])


menu = Menu(714, 798, screen)
fps = 60
timer = pygame.time.Clock()

run = True
mousemotion_event = None
while run:
    timer.tick(fps)
    menu.draw(mousemotion_event)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEMOTION:
            mousemotion_event = event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousemotion_event = event
        else: mousemotion_event = None

    pygame.display.flip()

pygame.quit()

# import pandas as pd
# leader_board = pd.read_csv("resources/leader_board.csv", sep=",")
#
# for i, item in leader_board.iterrows():
#     print(item)
#
# print("\n\n\n\n\n")
#
# leader_board = leader_board.sort_values(by="Time", sort_index=True)
# print(leader_board)
# print("\n\n\n")
#
# for i, item in leader_board.iterrows():
#     print(i, item)
