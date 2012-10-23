

class LamportClock():
	def __init__(self, addr, port):
		assert(port > 0)
		assert(len(addr.split('.')) == 4)
		self.lamportClock = 0.0
		self._setUniqueId(addr, port)
		
		
	#know it to run on a local network, only only changing the three last numbers
	def _setUniqueId(self, addr, port):
		lastDigit = str(addr).split('.')[-1]
		self.uniqeId = float('0.'+ lastDigit + str(port))
		self.lamportClock += self.uniqeId
		
	def synchClocks(self, clock):
		if self.isClockGreater(clock):
			self.lamportClock = int(float(clock)) + 1.0 + self.uniqeId

	def isClockGreater(self, clock):
		assert(clock != self.lamportClock)
		if clock > self.lamportClock:
			return True
		return False
		
	def increase(self):
		self.lamportClock += 1.0
		
	def getlamportClock(self):
		return self.lamportClock

if __name__ == "__main__":
	lp = LamportClock('127.0.0.12', 30667)
	lp.synchClocks('134.3')
	print lp.lamportClock
	lp.increase()
	print lp.lamportClock
	print lp.getlamportClock()