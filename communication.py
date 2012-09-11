# -*- coding: utf-8 -*-
import socket
import thread

class Listener():
  def __init__(self):
    self.host = socket.gethostname()
    
    self.sock = 