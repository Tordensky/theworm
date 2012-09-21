# -*- coding: utf-8 -*-
import commands
import communication
import shutil
import os




port = 30666
ip = 'localhost';


def deleteAllInFolder(folder):
	shutil.rmtree(folder)
	
class CellGate():
  def __init__(self):
    pass
  
  def startup(self):
    
    """
    Start up wormgate
    """
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
	try:
		cellgate = CellGate()
		cellgate.startup()
	except:
		deleteAllInFolder("/tmp/inf3200/asv009")

  