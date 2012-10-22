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


def quitPython():
	'''
	Method for quiting everything
	'''
	global RUNNING
	sys.stdout.flush()
	RUNNING = False
	os._exit(0)
	
class WormSegment():
	def __init__(self):
		"""
		The code for the worm segment 10,50
		"""
		self.sendHeartBeatIntervall = 100
		self.estimateHartBeatIntervall = 500
		self.heartbeatreciver = 0.0
		self.udpComm = UDPcomm(MCAST_PORT)
		self.numberOfSegments = 0
	
	def main(self):
		"""
		Running the main code for the worm
		"""
		self.listenForIncommingHeartBeats()
		thread.start_new_thread(self.sendHeartBeat,())
		boids = Graphics(quitPython, self.get_num_segments)
		thread.start_new_thread(boids.run, ())
		while RUNNING:
			time.sleep(self.estimateHartBeatIntervall/1000.0) # MS to seconds
			self.estimateNumberOfWormSegment()
			
	def propagate(self):
		"""
		This method is responsible for spreading itself to another node
		"""
		if RUNNING == True:
			target = TARGET_IPS[random.randint(0, len(TARGET_IPS) - 1)]
			communication.FileClient().sendFile( TMP_FOLDER +  "theworm.zip",target, WORM_GATE_PORT)
	
	def sendHeartBeat(self):
		"""
		Multicasts a heartbeat to all the rest of the worms
		"""
		while RUNNING:
			self.udpComm.send(self.sendHeartBeatIntervall)
			time.sleep(self.sendHeartBeatIntervall / 1000.0)
		
	
	def estimateNumberOfWormSegment(self):
		"""
		Estimates how many worms are in play 
		"""
		# NOTE Will get a race condition here, but we don't care about it since it's only a estimate
		self.numberOfSegments = self.heartbeatreciver/float(self.estimateHartBeatIntervall)
		self.numberOfSegments = math.ceil(self.numberOfSegments)
		self.heartbeatreciver = 0.0
		
		print "number of estimated segments" , self.numberOfSegments
		
		if self.numberOfSegments > MAX_WORM_SEGS:
			#self.shouldIKillMyself(self.numberOfSegments)
			pass
		elif self.numberOfSegments < MIN_WORM_SEGS:
			self.shouldIPropagate(self.numberOfSegments)

	def shouldIKillMyself(self, numberOfSegmentsAlive):
		'''
		Calculates the probability of a segment killing itself, gets a random value from 1 - 100 
		and checks if the value is inside the propability, meaning it should kill itself
		'''
		prosent = MAX_WORM_SEGS/numberOfSegmentsAlive * 100
		killAnswer = random.randrange(1, 101)
		
		if killAnswer >= prosent:
			self.killMySelf()

	def shouldIPropagate(self, numberOfSegmentsAlive):
		'''
		Calculates the probability if a segment should propagate, gets a random value from 1 - 100 
		and checks if the value is inside the propability, meaning it should spread
		'''
		prosent = numberOfSegmentsAlive/MIN_WORM_SEGS * 100
		propagateAnswer = random.randrange(1, 101)

		if propagateAnswer >= prosent:
			self.propagate()

	def listenForIncommingHeartBeats(self):
		"""
		Listen for all the heartbeats from the rest of the worm segments
		"""
		thread.start_new_thread(self.udpComm.listen,(10, self.killMySelf, self.updateHeartBeatCount))
	
	def get_num_segments(self):
		'''
		returns the latest measurement of number of segments alive
		'''
		return self.numberOfSegments
		
	def killMySelf(self):
		"""
		Simply stops all the python threads and quits
		"""
		quitPython()
		
	def updateHeartBeatCount(self, count):
		'''
		Updates heartbeat count
		'''
		self.heartbeatreciver += count


if __name__ == "__main__":
	
	#deamonize.daemonize('dev/null', 'output', 'error')
	os.putenv('DISPLAY', ':0') # Attach to local display

	worm = WormSegment()
	print "Startign the worm segment"
	worm.main()
	time.sleep(0.1); # Give display thread some time to terminate
