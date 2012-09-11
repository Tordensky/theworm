# -*- coding: utf-8 -*-
import commands

port = 30666
ip = 'localhost';

class CellGate():
  def __init__(self):
    pass
  
  def startup(self):
    """
    Start up wormgate
    """
    pass
  
  def listenForIncomingCells(self):
    """
    Listen for incoming segments
    """
    pass
  
    # TODO Receive new segments
  
  def becomeInefected(self):
    """
    Startup worm segment on host
    """
    pass
  
    # TODO startup new cell segment
    
  def die(self):
    """
    Stop worm gate
    """
    pass
  
    # TODO kill wormgate
  


if __name__ == "__main__":
  print "Staring wormgate"
  
  cmd = "python cells.py"
  
  res, text = commands.getstatusoutput( cmd )
  
  print "Returned status : %d" % res
  print "Returned text \n%s" % text