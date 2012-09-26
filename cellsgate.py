# -*- coding: utf-8 -*-
import commands
import communication
import shutil
import deamonize
import os
import sys
from config import *

def deleteAllInFolder(folder):
	shutil.rmtree(folder)
	
class CellGate():
  def __init__(self):
    pass
  
  def startup(self):
    
    """
    Start up wormgate
    """
    if os.path.exists(TMP_FOLDER):
    	deleteAllInFolder(TMP_FOLDER);
	
	os.makedirs(TMP_FOLDER)
    
   	deamonize.daemonize('dev/null', TMP_FOLDER + 'output', TMP_FOLDER + 'error')
    self.fileserver = communication.FileServer(LISTEN_PORT, WORM_GATE_PORT)
    self.fileserver.main();
    
    
  def die(self):
    """
    Stop worm gate
    """
    
    pass
  
    # TODO kill wormgate
  


if __name__ == "__main__":
	cellgate = CellGate()
	cellgate.startup()
	
