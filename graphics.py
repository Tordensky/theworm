'''
Created on Sep 26, 2012

@author: Simon
'''
import pygame, os, random
from config import *

class Graphics(object):
    def __init__(self):
        pygame.init()
        x = random.randint(0, 1024 - SCREEN_WIDTH)
        y = random.randint(0, 800 - SCREEN_HEIGHT)
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(x) + ',' + str(y)
    
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
    def run(self):
        while(1):
            pass
        
if __name__ == "__main__":
    graf = Graphics()
    graf.run()