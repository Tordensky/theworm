# -*- coding: utf-8 -*-
import os
import pygame
import random
import thread
import time
import deamonize
import sys
import communication
from udp import *
from config import *
from pygame.color import THECOLORS



def ChangeRunningToFalse():
	global RUNNING
	sys.stdout.flush()
	pygame.display.quit()
	RUNNING = False
	os._exit()
	
	
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
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				ChangeRunningToFalse()
				break
		clock.tick(100)
		myObject.update()    
		screen.fill((0, 0, 0))
		pygame.draw.rect(screen, pygame.color.THECOLORS['blue'], myObject.rect)
		pygame.display.update()
    print 'display thread terminated'



class WormSegment():
	def __init__(self):
		"""
		The code for the worm segment
		"""
		self.heartbeatreciver = 0.0
		self.udpComm = UDPcomm(MCAST_PORT)
	def main(self):
		"""
		Running the main code for the worm
		"""
		time.sleep(1)
		print self.heartbeatreciver
		self.propagate()
		time.sleep(5)
		print "i should have propagated" 
		self.killMySelf()
	
	def propagate(self):
		"""
		This fuction is responsible for spreading itself to another node
		"""
		
		if RUNNING == True:
			target = TARGET_IPS[random.randint(0, len(TARGET_IPS) - 1)]
			communication.FileClient().sendFile("/tmp/inf3200/asv009/theworm.zip",target, WORM_GATE_PORT)
		
	def sendHeartBeat(self):
		"""
		Broadcasts a heartbeat to all the rest of the worms
		"""
		pass
	
	def estimateNumberOfWormSegment(self):
		"""
		Estimates how many worms are in play 
		"""
		
		#Will get a raise condition here, but we don't care about it since it's only a estimate
		self.heartbeatreciver = 0.0
	
	def listenForIncommingHeartBeats(self):
		"""
		Listen for all the heartbeats from the rest of the worm segments
		"""
		
		thread.start_new_thread(self.udpComm.listen,(10, self.killMySelf, self.updateHeartBeatCount))
	
	def killMySelf(self):
		"""
		Simply stops all the python threads and quits
		"""
		ChangeRunningToFalse()
		
	def checkIfEmergencyKillSingalIsActive(self):
		"""
		Check if the kill file is active
		"""
		pass

	def updateHeartBeatCount(self, count):
		self.heartbeatreciver += count



if __name__ == "__main__":
	
	#Just to make the input file
	#new_file = open(path + '/input', 'w')
	#new_file.close()
	deamonize.daemonize('dev/null', 'output', 'error')
	
	thread.start_new_thread(display_worm_forever, ())
	worm = WormSegment()
	worm.listenForIncommingHeartBeats()
	
	print "I am running"

	while RUNNING:
		# TODO: Start implementing your worm here
		worm.main()
		print 'running...'
		time.sleep(1)
	time.sleep(0.1); # Give display thread some time to terminate