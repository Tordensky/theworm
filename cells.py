# -*- coding: utf-8 -*-
import os, pygame, random, thread, time, deamonize, sys, socket, struct
from pygame.color import THECOLORS


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
MAX_SPEED = 20
RUNNING = True

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 30667


MIN_SEGS = 5
MAX_SEGS = 10

TARGET_IPS = ['localhost'] 
WORM_GATE_PORT = 30666

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
        clock.tick(100)
        myObject.update()    
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, pygame.color.THECOLORS['blue'], myObject.rect)
        pygame.display.update()
    print 'display thread terminated'


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
			while True:
				received = self.reciveSock.recv(length)

				if received == 'die':
					die()
					return
				
				result (float(received))
				
                        
		except:
				print "some kind of weird error"
        

class WormSegment():
	def __init__(self):
		"""
		The code for the worm segment
		"""
		self.heartbeatreciver = 0.0
		self.udpComm = UDPcomm(MCAST_PORT)
	def main(self):
		"""
		Running the main code for the worm
		"""
		print self.heartbeatreciver
		self.propagate()
		time.sleep(2)
		self.killMySelf()
	
	def propagate(self):
		"""
		This fuction is responsible for spreading itself to another node
		"""
		target = TARGET_IPS[random.randint(0, len(TARGET_IPS) - 1)]
		communictation.FileClient().sendFile("theworm.zip",target, WORM_GATE_PORT)
	
	def sendHeartBeat(self):
		"""
		Broadcasts a heartbeat to all the rest of the worms
		"""
		pass
	
	def estimateNumberOfWormSegment(self):
		"""
		Estimates how many worms are in play 
		"""
		
		#Will get a raise condition here, but we don't care about it since it's only a estimate
		self.heartbeatreciver = 0.0
	
	def listenForIncommingHeartBeats(self):
		"""
		Listen for all the heartbeats from the rest of the worm segments
		"""
		
		thread.start_new_thread(self.udpComm.listen,(1024, self.updateHeartBeatCount, self.killMySelf))
	
	def killMySelf(self):
		"""
		Simply stops all the python threads and quits
		"""
		os._exit(1)

	def updateHeartBeatCount(self, count):
		self.heartbeatreciver += count

if __name__ == "__main__":
	
	path = '/tmp/inf3200/asv009/' + str(os.getpid())
	print path
	os.makedirs(path)
	
	#Just to make the input file
	#new_file = open(path + '/input', 'w')
	#new_file.close()
	
	deamonize.daemonize('dev/stdin', path + '/output', path +'/error')
	
	thread.start_new_thread(display_worm_forever, ())
	worm = WormSegment()
	worm.listenForIncommingHeartBeats()
	while RUNNING:
		# TODO: Start implementing your worm here
		worm.main()
		print 'running...'
		time.sleep(1)
	time.sleep(0.1); # Give display thread some time to terminate