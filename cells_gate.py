import commands

port = 30666
ip = 'localhost';

class CellGate():
  def __init__(self):
    pass
  


if __name__ == "__main__":
  print "Staring wormgate"
  
  cmd = "python cells.py"
  
  res, text = commands.getstatusoutput( cmd )
  
  print "Returned status : %d" % res
  print "Returned text \n%s" % text