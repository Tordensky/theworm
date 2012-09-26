# -*- coding: utf-8 -*-
import os
import pygame
import random
import thread
import time
import deamonize
import sys
import communication
import math
from udp import *
from config import *
from pygame.color import THECOLORS



def ChangeRunningToFalse():
	global RUNNING
	sys.stdout.flush()
	#pygame.display.quit()
	RUNNING = False
	os._exit(0)
	
	
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
		self.sendHeartBeatIntervall = 100
		self.estimateHartBeatIntervall = 500
		self.heartbeatreciver = 0.0
		self.udpComm = UDPcomm(MCAST_PORT)
	def main(self):
		"""
		Running the main code for the worm
		"""
		#time.sleep(1)
		#print self.heartbeatreciver
		#self.propagate()
		#time.sleep(5)
		self.listenForIncommingHeartBeats()
		thread.start_new_thread(self.sendHeartBeat,())
		while RUNNING:
			time.sleep(self.estimateHartBeatIntervall/1000.0)
			self.estimateNumberOfWormSegment()
			
			
	
	
	def propagate(self):
		"""
		This fuction is responsible for spreading itself to another node
		"""
		
		if RUNNING == True:
			target = TARGET_IPS[random.randint(0, len(TARGET_IPS) - 1)]
			communication.FileClient().sendFile( TMP_FOLDER +  "theworm.zip",target, WORM_GATE_PORT)
		
	def sendHeartBeat(self):
		"""
		Broadcasts a heartbeat to all the rest of the worms
		"""
		while RUNNING:
			self.udpComm.send(self.sendHeartBeatIntervall)
			time.sleep(self.sendHeartBeatIntervall / 1000.0)
		
	
	def estimateNumberOfWormSegment(self):
		"""
		Estimates how many worms are in play 
		"""
		
		#Will get a race condition here, but we don't care about it since it's only a estimate
		numberOfSegments = self.heartbeatreciver/float(self.estimateHartBeatIntervall)
		numberOfSegments = math.ceil(numberOfSegments)
		self.heartbeatreciver = 0.0
		
		print "number of estimated segments" , numberOfSegments
		
		if numberOfSegments > MAX_WORM_SEGS:
			self.shouldIKillMyself(numberOfSegments)
		elif numberOfSegments < MIN_WORM_SEGS:
			self.shouldIPropagate(numberOfSegments)

	def shouldIKillMyself(self, numberOfSegmentsAlive):
		#print "number of segs alive and max", numberOfSegmentsAlive, MAX_WORM_SEGS
		prosent = MAX_WORM_SEGS/numberOfSegmentsAlive * 100
		killAnswer = random.randrange(1, 101)
		
		print "killanswer and prosent: ", killAnswer, prosent
		if killAnswer >= prosent:
			self.killMySelf()

	def shouldIPropagate(self, numberOfSegmentsAlive):
		#print "number of segs alive and max", numberOfSegmentsAlive, MAX_WORM_SEGS
		prosent = numberOfSegmentsAlive/MIN_WORM_SEGS * 100
		propagateAnswer = random.randrange(1, 101)
		
		print "reproduceanswer and prosent: ", propagateAnswer, prosent
		if propagateAnswer >= prosent:
			self.propagate()


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
	
	deamonize.daemonize('dev/null', 'output', 'error')
	os.putenv('DISPLAY', ':0') # Attach to local display
	thread.start_new_thread(display_worm_forever, ())
	worm = WormSegment()
	
	print "Startign the worm segment"
	worm.main()
	time.sleep(0.1); # Give display thread some time to terminate