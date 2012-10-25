import json
import thread
import time
from lamport import *
from udp import *
from config import *

STATE_ASKFORLOCK = 1
STATE_TAKETHELOCK = 2
STATE_ANSWER_OK = 3
STATE_I_HAVE_THE_LOCK = 4
#The mutex only supports one critical section, for simplicity.The cricial section should always be the same place, may be extended in the future
#should be used only once for each worm segment
class Mutex():
	def __init__(self):
		self.hasLock= False
		self.udp = UDPcomm(0)
		#thread.start_new_thread(self.udp.listen,(1024, self._callback))
		self.multicast = UDPcomm(MCAST_PORT_MUTEX)
		thread.start_new_thread(self.multicast.listen,(1024, self._multicastCallback))
		
		self.lamport = LamportClock(self.udp.getMachineIp(), self.udp.getPort())
		
		
		self.waitingForLock = False
		self.askForLockOkCounter = 0
		self.lastLockRequestTime = 0.0
		self.lockQueue = []

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
		assert(self.hasLock == False)
		self.waitingForLock = True
		self._askForLock(getEstimatedSegmentsFunction)
		print "I have taken the lock"
			
	def unlock(self):
		if self.hasLock == False:
			return
		
		#I now unlock the lock, send the lock to the next one in the list, or all
		self.hasLock = False
		for waiters in self.lockQueue:
			print "sending to " + str(waiters)
			self.sendOK(waiters)
		
		self.lockQueue = []
		
	
	def _askForLock(self, getEstimatedSegmentsFunction):
		self.askForLockOkCounter = 0

		message = {}
		message["State"] = STATE_ASKFORLOCK
		message["TimeStamp"] = self.lamport.getlamportClock()
		message["Port"] = self.udp.getPort()
		self.lastLockRequestTime = self.lamport.getlamportClock()
		print "Sent an lock request with my time: " + str(self.lamport.getlamportClock())
		
		self.multicast.multicast(json.dumps(message))
		
		wormSegments = getEstimatedSegmentsFunction()
		print "number of segments is : " + str(wormSegments)
		self.lamport.increase() #MAY CREATE A DEADLOCK HERE
		
		try:
			while True:
				received = self.udp.socket.recv(1024)
				updates = json.loads(received, encoding='UTF-8')
				
				self.lamport.synchClocks(updates["TimeStamp"])
				
				if updates["State"] == STATE_ANSWER_OK:
					self.askForLockOkCounter += 1
					print "got an ok"  +  str(updates["TimeStamp"])
			
				if self.askForLockOkCounter == wormSegments:
					print "Got an ok from all"
					break
					
		except Exception as e:
			print "some kind of wierd listen mutex error"
			print e.args
		
		
		self.hasLock= True
		self.waitingForLock = False

	def _multicastCallback(self, data, addr):
		print data
		try:
			updates = json.loads(data, encoding='UTF-8')
		except Exception as e:
			print "json parse error"
			print e.args
			return
		
		updates["addr"] = addr[0]
		
		if updates["State"] == STATE_ASKFORLOCK:
			if self.hasLock == False:
				if self.waitingForLock == False:
					print "sending ok because i'm not interested"
					self.sendOK(updates)
				else:
					if self.lastLockRequestTime >= float(updates["TimeStamp"]):
						print "sendt ok"
						self.sendOK(updates)
					else:
						self.lockQueue.append(updates)
			else:
				self.lockQueue.append(updates)
			#self.lockQueue.append(updates)
		self.lamport.synchClocks(updates["TimeStamp"])
	
	def sendOK(self, message):
		newmessage = {}
		newmessage["State"] = STATE_ANSWER_OK
		newmessage["TimeStamp"] = self.lamport.getlamportClock()
		self.udp.send(json.dumps(newmessage), message["addr"], message["Port"])
		
		
	
	def getlamportClock(self):
		return self.lamport.getlamportClock()
		
#testing the udp
if __name__ == "__main__":
	mutex = Mutex()

	