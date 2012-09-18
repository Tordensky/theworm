import socket

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 30667

sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sendSock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)



sendSock.sendto("mordi", (MCAST_GRP, MCAST_PORT))