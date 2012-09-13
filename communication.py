# -*- coding: utf-8 -*-
import socket
import thread

class FileServer():
  def __init__(self, addr, port):
    self.host = socket.gethostname()
    
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    self.sock.bind((addr, port))
    
    self.sock.listen(5)
    
  def main(self):
    try:
      while 1:
	(connection, addr) = self.sock.accept()
	print "Client connected", connection, addr
	
	handler = FileHandler(connection)
	thread.start_new_thread(handler.main, ())
    except:
      print "some kind of weird error"
	
class FileHandler():
  def __init__(self, conn):
    print "mordi"
    self.conn = conn
    self.cfile = conn.makefile('rw', 0)
    
    
  def main(self):
    print "got some shit"
    line = self.cfile.readline().strip()
    print "--> REQUEST IS:", line
    

if __name__ == "__main__":
  print "Starting Server test"
  
  server = FileServer('localhost', 8080)
  server.main()