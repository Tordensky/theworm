MCAST_GRP = '224.1.1.1'
MCAST_PORT = 30667

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
MAX_SPEED = 20
RUNNING = True


TARGET_IPS = []
#for i in range(0,7):
	#for j in range(0,4):
		#TARGET_IPS.append('tile-%d-%d'%(i,j))
TARGET_IPS = ['localhost'] 

LISTEN_PORT = '0.0.0.0'
WORM_GATE_PORT = 30689

MAX_WORM_SEGS = 40
MIN_WORM_SEGS = 30 

TMP_FOLDER = "/tmp/inf3200/asv009/"