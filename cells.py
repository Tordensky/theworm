# -*- coding: utf-8 -*-
import os, pygame, random, thread, time, signal, deamonize, sys
from pygame.color import THECOLORS


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
MAX_SPEED = 20
RUNNING = True

#bad name for a sprite object
class MyObject(pygame.sprite.Sprite):  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.xadd = 5
        self.yadd = 5
        self.rect = pygame.rect.Rect(self.x, self.y, 25, 25)
              
    def update(self):
        self.x += self.xadd
        self.y += self.yadd
        
        if (self.x >= SCREEN_WIDTH - self.rect.width):
            self.xadd = -random.randint(1, MAX_SPEED)
        
        if (self.x <= 0):
            self.xadd = random.randint(1, MAX_SPEED)
            
        if (self.y >= SCREEN_HEIGHT - self.rect.height):
            self.yadd = -random.randint(1, MAX_SPEED)
            
        if (self.y <= 0):
            self.yadd = random.randint(1, MAX_SPEED)
        
        self.rect.topleft = (self.x, self.y)

#should change this to display somethign else
def display_worm_forever():
    x = random.randint(0, 1024 - SCREEN_WIDTH)
    y = random.randint(0, 800 - SCREEN_HEIGHT)
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(x) + ',' + str(y)
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

    clock = pygame.time.Clock()
    myObject = MyObject()        
    while RUNNING:
        clock.tick(100)
        myObject.update()    
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, pygame.color.THECOLORS['blue'], myObject.rect)
        pygame.display.update()
    print 'display thread terminated'


#class Worm():
	#def __init__


if __name__ == "__main__":
	
	path = '/tmp/inf3200/asv009/' + str(os.getpid())
	os.mkdir(path)
	
	#Just to make the input file
	new_file = open(path + '/input', 'w')
	new_file.close()
	
	deamonize.daemonize(path + '/input', path + '/output', path +'/error')
	
	thread.start_new_thread(display_worm_forever, ())
    
	while RUNNING:
		# TODO: Start implementing your worm here
        
		print 'running...'
		time.sleep(1)
	time.sleep(0.1); # Give display thread some time to terminate