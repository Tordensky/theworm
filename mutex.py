import json
import thread
import time
from lamport import *
from udp import *
from config import *

STATE_ASKFORLOCK = 1
STATE_TAKETHELOCK = 2
#The mutex only supports one critical section, for simplicity.The cricial section should always be the same place, may be extended in the future
#should be used only once for each worm segment
class Mutex():
	def __init__(self):
		self.hasLock= False
		self.udp = UDPcomm(0)
		thread.start_new_thread(self.udp.listen,(1024, self._callback))
		self.multicast = UDPcomm(MCAST_PORT_MUTEX)
		thread.start_new_thread(self.multicast.listen,(1024, self._multicastCallback))
		
		self.lamport = LamportClock(self.udp.getMachineIp(), self.udp.getPort())
		

		self.doesAnyOneHaveTheLock = True
		
		self.askForLockOkCounter = 0

	def run(self, getEstimatedSegmentsFunction):
		while(True):
			time.sleep(1) # Random
			print "Trying to lock"
			self.lock(getEstimatedSegmentsFunction)
			print "Sleeping a little"
			time.sleep(2) # Should be more random, change in future
			
			print "Unlocking"
			self.unlock()

	def lock(self, getEstimatedSegmentsFunction):
		print self.hasLock
		assert(self.hasLock == False)
		if self._askForLock(getEstimatedSegmentsFunction):
			#self.hasLock = True
			print "haslock"

	def unlock(self):
		if self.hasLock == True:
			return
	
	def _askForLock(self, getEstimatedSegmentsFunction):
		self.askForLockOkCounter = 0
		
		message = {}
		message["State"] = STATE_ASKFORLOCK
		message["TimeStamp"] = self.lamport.getlamportClock()
		
		self.multicast.multicast(json.dumps(message))
		wormSegments = getEstimatedSegmentsFunction()
		
		self.lamport.increase()
		
	
		
		now = time.time()
		future = now + 1
		while time.time() < future:
			if self.askForLockOkCounter > 0.75 * wormSegments:
				print "got an ok from more then half"
				#should take the lock now
				return True
			
		return False
		#TODO:
		#	ask for lock
		#	check if more then half or bigger says ok
		#	check if someone else has 
	
	def _takeTheLock(self, getEstimatedSegmentsFunction):
		#TODO: Actually take the lock
		#Say you take the lock
		#If more then half got that, you take the lock
		#if not half got that restart the whole process or kill yourself
		pass
	

	def _callback(self, data):
		pass
	
	def _multicastCallback(self, data):
		print data
		updates = json.loads(data, encoding='UTF-8')
		self.lamport.synchClocks(updates["TimeStamp"])
		
	def getlamportClock(self):
		return self.lamport.getlamportClock()
		
#testing the udp
if __name__ == "__main__":
	mutex = Mutex()

	