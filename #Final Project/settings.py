
import pygame

import pygame.font

pygame.init()


class Settings():

    def __init__(self):

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.yellow = (255, 255, 0)
        self.green = (0, 255, 0)
        self.green1 = (0, 150, 20)
        self.green2 = (0, 80, 0)
        self.green3 = (110, 255, 0)
        self.red = (255, 0, 0)
        self.red2 = (160, 0, 0)
        self.maroon = (80, 0, 20)
        self.gray = (5, 5, 5)
        self.gray2 = (70, 70, 70)
        self.gray3 = (10, 10, 10)

        #self.screen = screen
        self.screen_width = 288
        self.screen_height = 512
        self.bg_color = self.gray

        self.titleFont = pygame.font.Font("halken.otf", 38)
        self.titleFont2 = pygame.font.Font("halkeno.otf", 42)
        self.titleFont3 = pygame.font.Font("halkeng.otf", 38)
        self.noteFont = pygame.font.SysFont("arial", 55)

        # button
        self.font_size = 50
        self.buttonx = 0
        self.buttony = 188
        self.button_width = 288
        self.button_height = 100

    def draw(self, screen): # lines for measuring and calibration

        # far left lines
        pygame.draw.line(screen, self.green2, (11, 290), (11, 310))
        pygame.draw.line(screen, self.green1, (7, 292.5), (7, 307.5))
        pygame.draw.line(screen, self.green, (3, 295), (3, 305))
        # far right lines
        pygame.draw.line(screen, self.maroon, (self.screen_width - 11, 290), (self.screen_width - 11, 310))
        pygame.draw.line(screen, self.red2, (self.screen_width - 7, 292.5), (self.screen_width - 7, 307.5))
        pygame.draw.line(screen, self.red, (self.screen_width - 3, 295), (self.screen_width - 3, 305))
        # centre lines
        pygame.draw.line(screen, self.white, (11, 300), (self.screen_width - 11, 300))
        pygame.draw.line(screen, self.gray2, (11, 297), (self.screen_width - 11, 297))
        pygame.draw.line(screen, self.gray2, (11, 303), (self.screen_width - 11, 303))
        pygame.draw.line(screen, self.gray3, (11, 294), (self.screen_width - 11, 294))
        pygame.draw.line(screen, self.gray3, (11, 306), (self.screen_width - 11, 306))

