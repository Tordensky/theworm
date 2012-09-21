# -*- coding: utf-8 -*-
import socket
import thread
import sys
import commands
import os
import time
from udp import *
from config import *

TYPE_FILE = '1'
NumberOfWormsStarted = 0




class FileServer():
	def __init__(self, addr, port):
		self.host = socket.gethostname()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((addr, port))
		self.sock.listen(5)

	def main(self):
		try:
			while True:
				(connection, addr) = self.sock.accept()
				print "Client connected", connection, addr
				handler = FileHandler(connection)
				thread.start_new_thread(handler.main, ())
				
		except Exception as e:
			#print e.args
			print "Some kind of weird error:"


class FileClient():
	
	@staticmethod
	def readBytesFromFile(filepath):
		tmpBuffer = ""
		try:
			print "printing : " + filepath
			tmpBuffer += open(filepath, 'r').read()
			
		except:
			print "File load Error"
			print sys.exc_info()
		return tmpBuffer
    

		
	@staticmethod
	def sendFile(filepath, addr, port):
		dataBuffer = FileClient.readBytesFromFile(filepath)
		message = MessageHandler.buildMessage(dataBuffer)
		
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
		self.saveDataToFile("/tmp/inf3200/asv009/theworm.zip", dataDict["Payload:"])
		self.runCode()
		print "Got data, unziped it and made it run"
    
	def runCode(self):
		global NumberOfWormsStarted
		os.makedirs("/tmp/inf3200/asv009/" + str(NumberOfWormsStarted))
		res, text = commands.getstatusoutput( "unzip -o /tmp/inf3200/asv009/theworm.zip -d /tmp/inf3200/asv009/" + str(NumberOfWormsStarted) )
		res, text = commands.getstatusoutput("python /tmp/inf3200/asv009/" + str(NumberOfWormsStarted) + "/cells.py")
		NumberOfWormsStarted += 1
			
		
	def saveDataToFile(self, filename, data):
		try:
			new_file = open(filename, 'w')
			new_file.write(data)
			new_file.close()
		except:
			print "File save error"
			print sys.exc_info()
		print "Saved file at: " + filename
                    

	

#testing the communication, needs the file at the location tough
if __name__ == "__main__":
	#send in more arguments to make the client run, insert nothing to get the server to run
	if len(sys.argv) == 2:
		print "Starting Client test"
		FileClient.sendFile("theworm.zip", 'localhost', 30666)
		
	else:
		print "Starting Server test"
		server = FileServer('localhost', 30666)
		server.main()