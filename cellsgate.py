# -*- coding: utf-8 -*-
from commands import *
import communication
import shutil
import deamonize
import os
import sys
from config import *
import time
import thread
import pygame
import random

def deleteAllInFolder(folder):
	'''
	Deletes all the files and folders in the given path
	'''
	shutil.rmtree(folder)
		
class CellGate():
	'''
	The worm gate
	'''
	def __init__(self):
		'''
		Constructor
		'''
		self.numberofwormsstarted = 0
	
	def showWormGateWindow(self):
		'''
		Displays a pygame window wit random colors displaying the number of segments started
		'''
		pygame.init()
		x = 150
		y = 0
		os.environ['SDL_VIDEO_WINDOW_POS'] = str(x) + ',' + str(y)
		self.screen = pygame.display.set_mode((150, 150))    
		SCREEN_COLOR = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
		color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
		myFont = pygame.font.SysFont("None", 100)
		
		clock = pygame.time.Clock()
		while(True):
				for event in pygame.event.get():
						if event.type == pygame.QUIT:
								sys.stdout.flush()
								os._exit(0)
				pygame.draw.rect(self.screen, (SCREEN_COLOR), (0, 0, self.screen.get_width(), self.screen.get_height()))
				time_passed = clock.tick(5) # limit to x FPS 
				self.screen.blit(myFont.render(str(self.numberofwormsstarted), 0, (color)), (10,10))
				pygame.display.update()
	
	def startup(self):  
		"""
		Start up wormgate
		"""

		if os.path.exists(TMP_FOLDER):
				deleteAllInFolder(TMP_FOLDER);
		
		os.makedirs(TMP_FOLDER)
		
		deamonize.daemonize('dev/null', TMP_FOLDER + 'output', TMP_FOLDER + 'error')
		thread.start_new_thread(self.die,())
		
		thread.start_new_thread(self.showWormGateWindow, ())
		
		self.fileserver = communication.FileServer(LISTEN_PORT, WORM_GATE_PORT)
		self.fileserver.main(self.setNumberOfStartedSegmets)
		
	def setNumberOfStartedSegmets(self, number):
		'''
		Sets the total number of startet segments
		'''
		self.numberofwormsstarted = number
			
	def die(self):
		"""
		Stop worm gate in case of big emergencies
		"""
		while(True):
				rows = getoutput("pgrep -f cells").split("\n")
				if len(rows) > (MAX_WORM_SEGS * 2):
						getoutput("killall python")
				# TODO kill wormgate
				time.sleep(0.5)
		


if __name__ == "__main__":
		cellgate = CellGate()
		cellgate.startup()
		
