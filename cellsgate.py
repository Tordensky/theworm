# -*- coding: utf-8 -*-
import commands
import communication
import shutil
import deamonize
import os
import sys



port = 30689
ip = '0.0.0.0';


def deleteAllInFolder(folder):
	shutil.rmtree(folder)
	
class CellGate():
  def __init__(self):
    pass
  
  def startup(self):
    
    """
    Start up wormgate
    """
    if not os.path.exists("/tmp/inf3200/asv009/"):
    	os.makedirs("/tmp/inf3200/asv009/")
   
    self.fileserver = communication.FileServer(ip, port)
    self.fileserver.main();
    
    
  def die(self):
    """
    Stop worm gate
    """
    
    pass
  
    # TODO kill wormgate
  


if __name__ == "__main__":
	deamonize.daemonize()
	cellgate = CellGate()
	cellgate.startup()
	
