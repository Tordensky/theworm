import socket
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 30667

sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sendSock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)


for i in range (0,10):
	sendSock.sendto("die", (MCAST_GRP, MCAST_PORT))
	time.sleep(0.1)
