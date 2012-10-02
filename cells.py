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
from graphics import * 


def ChangeRunningToFalse():
	global RUNNING
	sys.stdout.flush()
	#pygame.display.quit()
	RUNNING = False
	os._exit(0)
	



class WormSegment():
	def __init__(self):
		"""
		The code for the worm segment
		"""
		self.sendHeartBeatIntervall = 20
		self.estimateHartBeatIntervall = 200
		self.heartbeatreciver = 0.0
		self.udpComm = UDPcomm(MCAST_PORT)
		self.numberOfSegments = 0
	def main(self):
		"""
		Running the main code for the worm
		"""

		self.listenForIncommingHeartBeats()
		thread.start_new_thread(self.sendHeartBeat,())
		boids = Graphics(ChangeRunningToFalse, self.get_num_segments)
		thread.start_new_thread(boids.run, ())
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
			#if self.numberOfSegments <= 1:
				#for i in range(0, BUCKET_SHOT):
					#print i
					#self.sendWormSegment()
			#else:
				#self.sendWormSegment()			
	
	def sendWormSegment(self):
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
		self.numberOfSegments = self.heartbeatreciver/float(self.estimateHartBeatIntervall)
		self.numberOfSegments = math.ceil(self.numberOfSegments)
		self.heartbeatreciver = 0.0
		
		print "number of estimated segments" , self.numberOfSegments
		
		if self.numberOfSegments > MAX_WORM_SEGS:
			self.shouldIKillMyself(self.numberOfSegments)
		elif self.numberOfSegments < MIN_WORM_SEGS:
			self.shouldIPropagate(self.numberOfSegments)

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
	
	def get_num_segments(self):
		return self.numberOfSegments
		
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

	
	worm = WormSegment()
	print "Startign the worm segment"
	worm.main()
	time.sleep(0.1); # Give display thread some time to terminate