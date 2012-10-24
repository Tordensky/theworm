# -*- coding: utf-8 -*-
import socket
import struct
from config import *
import socket




class UDPcomm():
	'''
	Class for UDP communictation
	Based the code on what found at: http://stackoverflow.com/questions/603852/multicast-in-python
	'''
	def __init__(self, PORT):
		'''
		constructor
		'''
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('', PORT))
		mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
		self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	
		self.multicastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.multicastSock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		self.port = self.socket.getsockname()[1]
	
	@staticmethod
	def getMachineIp():
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('rocksvv.cs.uit.no', 0))
		return s.getsockname()[0]
		
	def getPort(self):
		return self.port
		
	def send(self, data, addr, port):
		'''
		sends data at the given addr/port
		'''
		self.socket.sendto(str(data), (addr, port))

	def multicast(self,data):
		'''
		sends data at the given mulicast addr/port
		'''
		self.multicastSock.sendto(str(data), (MCAST_GRP, self.port))

	def listen(self, length, callback):
		'''
		listen for incoming datagrams
		'''
		try:
			while True:
				received, addr = self.socket.recvfrom(length)
				callback(received, addr)
				

		except Exception as e:
				print "some kind of wierd upd error"
				print e.args



#testing the udp
if __name__ == "__main__":
	def callback(recived):
		print recived
	import thread
	udp = UDPcomm(0)
	#thread.start_new_thread(udp.listen,(10, callback))
	print udp.getMachineIp()
	#udpMUL = UDPcomm(MCAST_PORT_MUTEX)
	#thread.start_new_thread(udpMUL.listen,(10, callback))
	
	#udp.send("mordi", udp.socket.getsockname()[0], udp.socket.getsockname()[1])
	#udpMUL.multicast("fardi")
	#udp.send("mordi2", udp.socket.getsockname()[0], udp.socket.getsockname()[1])
	
	
	while(1):
		pass
	#udp.listen()