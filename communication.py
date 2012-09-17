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
        self.conn = conn
    
        self.cfile = conn.makefile('rw', 0)
    
    def main(self):
        line = self.cfile.readline().strip()
    
        print "Request is:", line
    
    def DataToDict(self):
        self.dataDict = {}
        
        while(True):
            
            line = self.cfile.readline()
        
            if not line.strip():
                try:
                    self.dataDict["payload"] = self.cfile.readline(int(self.dataDict["Size:"]))
                    break
                except:
                    print "unvalid message"
                    break
            else:
                self.dataDict[line.split()[0]] = line.split()[1]
                
    def saveDataToFile(self, filename, data):
        try:
            new_file = open("/tmp/" + filename, 'w')
            
            f.write(data)
            
            f.close
        except:
            print "File error"
                    
    
if __name__ == "__main__":
    print "Starting Server test"

    server = FileServer('localhost', 8080)

    server.main()