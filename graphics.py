# -*- coding: utf-8 -*-
import pygame, os, random
from config import *
from miniboids import *

class Graphics(object):
	def __init__(self, dieFunction, number_of_segments):
		'''
		constructor
		'''
		self.dieFunction = dieFunction
		self.num_segs = number_of_segments
		
	def run(self):
		'''
		starts the simple boids simulation
		'''
		
		pygame.init()
		x = random.randint(0, 1024 - SCREEN_WIDTH)
		y = random.randint(0, 800 - SCREEN_HEIGHT)
		os.environ['SDL_VIDEO_WINDOW_POS'] = str(x) + ',' + str(y)
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		
		# How many boids to simulate
		boids = []
		for x in range(random.randrange(5, 10)):        
			boids.append(Boid(self.screen))
	
			
		clock = pygame.time.Clock()
		SCREEN_COLOR = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
		
		myFont = pygame.font.SysFont("None", 300)
		color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
		
		while(RUNNING):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.dieFunction()
			
			pygame.draw.rect(self.screen, (SCREEN_COLOR), (0, 0, self.screen.get_width(), self.screen.get_height()))
			time_passed = clock.tick(30) # limit to x FPS 
			time_passed_seconds = time_passed / 1000.0

			self.screen.blit(myFont.render(str(int(self.num_segs())), 0, (color)), (10,10))
			
			# Update boids
			for boid in boids:
				boid.update_vectors(boids,[], [])
				boid.move(time_passed_seconds, self.screen)
				boid.draw(self.screen)
			

			pygame.display.update()



def num():
	'''
	Method for testing
	'''
	return 1            
		
if __name__ == "__main__":
	graf = Graphics(1, num)
	graf.run()