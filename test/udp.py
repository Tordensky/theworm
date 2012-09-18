# -*- coding: utf-8 -*-
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="B Fjukstad, University of Troms"
__date__ ="$Aug 20, 2010 1:22:51 PM$"

# Code from http://docs.python.org/library/socketserver.html

import socket
import sys

HOST, PORT = "localhost", 30667

HOST = sys.argv[1]
PORT = int( sys.argv[2] )
    
data = " ".join(sys.argv[3:])

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().

sock.sendto(data + "\n", (HOST, PORT))


print "Sent:     %s" % data
