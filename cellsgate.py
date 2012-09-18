# -*- coding: utf-8 -*-
import commands
import communication

port = 30666
ip = 'localhost';

class CellGate():
  def __init__(self):
    pass
  
  def startup(self):
    
    """
    Start up wormgate
    """
    self.fileserver = communication.FileServer(ip, port)
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

  