# -*- coding: utf-8 -*-
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="B Fjukstad, University of Tromso"
__date__ ="$Aug 20, 2010 1:52:30 PM$"

# Code from http://docs.python.org/library/socketserver.html

import SocketServer

class MyThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print "%s wrote:" % self.client_address[0]
        print data
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "", 9999
    print "Server is listening on port %d" % PORT
    
    server = MyThreadedUDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()