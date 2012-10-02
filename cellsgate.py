# -*- coding: utf-8 -*-
from commands import *
import communication
import shutil
import deamonize
import os
import sys
from config import *
import time
import thread
import pygame

def deleteAllInFolder(folder):
	shutil.rmtree(folder)
	
class CellGate():
  def __init__(self):
    self.numberofwormsstarted = 0;
  
  def showWormGateWindow():
	pygame.init()
	x = random.randint(0, 1024 - SCREEN_WIDTH)
	y = random.randint(0, 800 - SCREEN_HEIGHT)
	os.environ['SDL_VIDEO_WINDOW_POS'] = str(x) + ',' + str(y)
	self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
  
  def startup(self):
    
    """
    Start up wormgate
    """

    if os.path.exists(TMP_FOLDER):
    	deleteAllInFolder(TMP_FOLDER);
	
	os.makedirs(TMP_FOLDER)
    
   	deamonize.daemonize('dev/null', TMP_FOLDER + 'output', TMP_FOLDER + 'error')
    thread.start_new_thread(self.die,())
    
    thread.start_new_thread(boids.run, ())
		
    
    self.fileserver = communication.FileServer(LISTEN_PORT, WORM_GATE_PORT)
    self.fileserver.main();
    
    
  def die(self):
    """
    Stop worm gate in case of big emergencies
    """
    while(True):
		rows = getoutput("pgrep -f cells").split("\n")
		if len(rows) > (MAX_WORM_SEGS * 2):
			getoutput("killall python")
		# TODO kill wormgate
		time.sleep(0.5)
	


if __name__ == "__main__":
	cellgate = CellGate()
	cellgate.startup()
	
