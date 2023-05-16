# # # import pygame
# # #
# # # from gui.Menu.Menu import Menu
# # #
# # # pygame.init()
# # # screen = pygame.display.set_mode([714, 798])
# # #
# # #
# # # menu = Menu(714, 798, screen)
# # # fps = 60
# # # timer = pygame.time.Clock()
# # #
# # # run = True
# # # mousemotion_event = None
# # # while run:
# # #     timer.tick(fps)
# # #     menu.draw(mousemotion_event)
# # #
# # #     for event in pygame.event.get():
# # #         if event.type == pygame.QUIT:
# # #             run = False
# # #         elif event.type == pygame.MOUSEMOTION:
# # #             mousemotion_event = event
# # #         elif event.type == pygame.MOUSEBUTTONDOWN:
# # #             mousemotion_event = event
# # #         else: mousemotion_event = None
# # #
# # #     pygame.display.flip()
# # #
# # # pygame.quit()
# # #
# # # # import pandas as pd
# # # # leader_board = pd.read_csv("resources/leader_board.csv", sep=",")
# # # #
# # # # for i, item in leader_board.iterrows():
# # # #     print(item)
# # # #
# # # # print("\n\n\n\n\n")
# # # #
# # # # leader_board = leader_board.sort_values(by="Time", sort_index=True)
# # # # print(leader_board)
# # # # print("\n\n\n")
# # # #
# # # # for i, item in leader_board.iterrows():
# # # #     print(i, item)
# #
# #
# # # import sys module
# # import pygame
# # import sys
# #
# # # pygame.init() will initialize all
# # # imported module
# # pygame.init()
# #
# # clock = pygame.time.Clock()
# #
# # # it will display on screen
# # screen = pygame.display.set_mode([600, 500])
# #
# # # basic font for user typed
# # base_font = pygame.font.Font(None, 32)
# # user_text = ''
# #
# # # create rectangle
# # input_rect = pygame.Rect(200, 200, 140, 32)
# #
# # # color_active stores color(lightskyblue3) which
# # # gets active when input box is clicked by user
# # color_active = pygame.Color('lightskyblue3')
# #
# # # color_passive store color(chartreuse4) which is
# # # color of input box.
# # color_passive = pygame.Color('chartreuse4')
# # color = color_passive
# #
# # active = False
# #
# # while True:
# #     for event in pygame.event.get():
# #
# #         # if user types QUIT then the screen will close
# #         if event.type == pygame.QUIT:
# #             pygame.quit()
# #             sys.exit()
# #
# #         if event.type == pygame.MOUSEBUTTONDOWN:
# #             if input_rect.collidepoint(event.pos):
# #                 active = True
# #             else:
# #                 active = False
# #
# #         if event.type == pygame.KEYDOWN:
# #
# #             # Check for backspace
# #             if event.key == pygame.K_BACKSPACE:
# #
# #                 # get text input from 0 to -1 i.e. end.
# #                 user_text = user_text[:-1]
# #
# #             # Unicode standard is used for string
# #             # formation
# #             else:
# #                 user_text += event.unicode
# #
# #     # it will set background color of screen
# #     screen.fill((255, 255, 255))
# #
# #     if active:
# #         color = color_active
# #     else:
# #         color = color_passive
# #
# #     # draw rectangle and argument passed which should
# #     # be on screen
# #     pygame.draw.rect(screen, color, input_rect)
# #
# #     text_surface = base_font.render(user_text, True, (255, 255, 255))
# #
# #     # render at position stated in arguments
# #     screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
# #
# #     # set width of textfield so that text cannot get
# #     # outside of user's text input
# #     input_rect.w = max(100, text_surface.get_width() + 10)
# #
# #     # display.flip() will update only a portion of the
# #     # screen to updated, not full area
# #     pygame.display.flip()
# #
# #     # clock.tick(60) means that for every second at most
# #     # 60 frames should be passed.
# #     clock.tick(60)
#
# import pygame as pg
#
#
# pg.init()
# screen = pg.display.set_mode((640, 480))
# COLOR_INACTIVE = pg.Color('lightskyblue3')
# COLOR_ACTIVE = pg.Color('dodgerblue2')
# FONT = pg.font.Font(None, 32)
#
#
# class InputBox:
#
#     def __init__(self, x, y, w, h, text=''):
#         self.rect = pg.Rect(x, y, w, h)
#         self.color = COLOR_INACTIVE
#         self.text = text
#         self.txt_surface = FONT.render(text, True, self.color)
#         self.active = False
#
#     def handle_event(self, event):
#         if event.type == pg.MOUSEBUTTONDOWN:
#             # If the user clicked on the input_box rect.
#             if self.rect.collidepoint(event.pos):
#                 # Toggle the active variable.
#                 self.active = not self.active
#             else:
#                 self.active = False
#             # Change the current color of the input box.
#             self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
#         if event.type == pg.KEYDOWN:
#             if self.active:
#                 if event.key == pg.K_RETURN:
#                     print(self.text)
#                     self.text = ''
#                 elif event.key == pg.K_BACKSPACE:
#                     self.text = self.text[:-1]
#                 else:
#                     self.text += event.unicode
#                 # Re-render the text.
#                 self.txt_surface = FONT.render(self.text, True, self.color)
#
#     def update(self):
#         # Resize the box if the text is too long.
#         width = max(200, self.txt_surface.get_width()+10)
#         self.rect.w = width
#
#     def draw(self, screen):
#         # Blit the text.
#         screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
#         # Blit the rect.
#         pg.draw.rect(screen, self.color, self.rect, 2)
#
#
#
# def main():
#     clock = pg.time.Clock()
#     input_box1 = InputBox(100, 100, 140, 32)
#     input_box2 = InputBox(100, 300, 140, 32)
#     input_boxes = [input_box1, input_box2]
#     done = False
#
#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             for box in input_boxes:
#                 box.handle_event(event)
#
#         for box in input_boxes:
#             box.update()
#
#         screen.fill((30, 30, 30))
#         for box in input_boxes:
#             box.draw(screen)
#
#         pg.display.flip()
#         clock.tick(30)
#
#
# if __name__ == '__main__':
#     main()
#     pg.quit()

import datetime
def get_str_time(time):
    delta = datetime.timedelta(seconds=time)
    str_time = str(delta).split(".")[0]  # delete milisecond

    length_delta = 8 - len(str_time)
    if length_delta > 0:
        str_time = '0' * length_delta + str_time
    return str_time

