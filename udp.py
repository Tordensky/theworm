import socket
import struct
from config import *

class UDPcomm():
    '''
    Class for UDP communictation
    found some implementation http://stackoverflow.com/questions/603852/multicast-in-python
    '''
    def __init__(self, PORT):
		self.reciveSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.reciveSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.reciveSock.bind(('', MCAST_PORT))
		mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
		self.reciveSock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
		self.sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sendSock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		self.port = PORT
		
    def send(self, data):
        self.senSock.sendto(data, (MCAST_GRP, self.port))

    def listen(self, length, result, die):
		try:
			while RUNNING:
				received = self.reciveSock.recv(length)

				if received == 'die':
					die()
					return
				
				result (float(received))
				
                        
		except:
				print "some kind of weird error"
        