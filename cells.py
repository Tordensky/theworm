# -*- coding: utf-8 -*-
import pygame 
from pygame.locals import *

pygame.init()

screen_res = (1024, 768)

screen = pygame.display.set_mode((screen_res), 0, 32)


while True:
        for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if event.type == QUIT or key[pygame.K_ESCAPE]:
                        exit()

        pygame.display.update()