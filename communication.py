# -*- coding: utf-8 -*-
import socket
import thread
import sys

TYPE_FILE = '1'

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

class FileClient():
	
	@staticmethod
	def readBytesFromFile(filepath):
		tmpBuffer = ""
		try:
			print "printing : " + filepath
			tmpBuffer += open(filepath, 'rU+').read()
			#data_file = File.open(filepath, 'rU')  
			#while(True):
				#bytes = data_file.read(5)
				#if bytes:
					#tmpBuffer += bytes
				#else:
					#break
		except:
			print "File load Error"
			print sys.exc_info()
		#Testign that the file is correct
		print tmpBuffer
		return tmpBuffer
    

		
	@staticmethod
	def sendFile(filepath, addr, port):
		dataBuffer = FileClient.readBytesFromFile(filepath)
		message = MessageHandler.buildMessage(dataBuffer)
		print message
		try:    
			cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			cs.connect((addr, port))
			cs.send(message)
			cs.close()
		except:
			print "Error while sending file"
                

class MessageHandler():
    
	@staticmethod
	def buildMessage(dataBuffer):
		message = (("Type: " + TYPE_FILE + "\n") +
					("Size: " + str(len(dataBuffer)) + "\n") +
					("\n" + dataBuffer))
		return message

	@staticmethod
	def DataToDict(cfile):
		dataDict = {}
		
		while(True):    
			line = cfile.readline()
			if not line.strip():
				try:
					dataDict["Payload:"] = cfile.read(int(dataDict["Size:"]))
					break
				except:
					print "unvalid message"
					break
			else:
				dataDict[line.split()[0]] = line.split()[1]
		return dataDict

                
class FileHandler():
	def __init__(self, conn):
		self.conn = conn
		self.cfile = conn.makefile('rw', 0)
    
	def main(self):
		dataDict = MessageHandler.DataToDict(self.cfile)
		print dataDict["Payload:"]
		self.saveDataToFile("/tmp/inf3200/asv009/recived.zip", dataDict["Payload:"])
    
    
                
	def saveDataToFile(self, filename, data):
		try:
			new_file = open(filename, 'w+')
			new_file.write(data)
			new_file.close
		except:
			print "File save error"
			print sys.exc_info()
		print "Saved file at: " + filename
                    
    
if __name__ == "__main__":
	if len(sys.argv) == 2:
		print "Starting Client test"
		FileClient.sendFile("/tmp/inf3200/asv009/test.zip", 'localhost', 8080)
	else:
		print "Starting Server test"
		server = FileServer('localhost', 8080)
		server.main()