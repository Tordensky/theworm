# -*- coding: utf-8 -*-
import socket
import thread
import sys
import commands
import os
import time
import random
from udp import *
from config import *

TYPE_FILE = '1'
NumberOfWormsStarted = 0

class FileServer():
	'''
	Class for starting a simple file server
	'''
	def __init__(self, addr, port):
		'''
		Constructor
		'''
		self.host = socket.gethostname()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print addr, port
		self.sock.bind((addr, port))
		self.sock.listen(5)

	def main(self, setNumberOfStartedSegmets):
		'''
		Start listeing for incoming request/files
		'''
		try:
			while True:
				(connection, addr) = self.sock.accept()
				print "Client connected", connection, addr
				handler = FileHandler(connection, setNumberOfStartedSegmets)
				thread.start_new_thread(handler.main, ())
				
		except Exception as e:
			#print e.args
			print "Some kind of weird error:"


class FileClient():
	'''
	A simple client for sending files
	'''
	@staticmethod
	def readBytesFromFile(filepath):
		tmpBuffer = ""
		try:
			print "printing : " + filepath
			tmpBuffer += open(filepath, "rb").read()
			
		except:
			print "File load Error"
			print sys.exc_info()
		return tmpBuffer
	
	@staticmethod
	def sendFile(filepath, addr, port):
		'''
		sends a given file to given address and port
		'''
		dataBuffer = FileClient.readBytesFromFile(filepath)
		message = MessageHandler.buildMessage(dataBuffer)
		
		try:    
			cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			cs.connect((addr, port))
			cs.send(message)
			cs.close()
		except:
			print "Error while sending file"
			print "addr: %s port %d" % (addr, port)
			print sys.exc_info()
				

class MessageHandler():
	'''
	Helper class for handling file messages
	'''
	@staticmethod
	def buildMessage(dataBuffer):
		'''
		Building a message
		'''
		message = (("Type: " + TYPE_FILE + "\n") +
					("Size: " + str(len(dataBuffer)) + "\n") +
					("\n" + dataBuffer))
		return message

	@staticmethod
	def DataToDict(cfile):
		'''
		Parsing a message
		'''
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
	'''
	The handler for the fileserver
	'''
	def __init__(self, conn, setNumberOfStartedSegmets):
		'''
		constructor
		'''
		self.conn = conn
		self.cfile = conn.makefile('rw', 0)
		self.setNumberOfStartedSegmets = setNumberOfStartedSegmets
	
	def main(self):
		'''
		Saves the incoming file
		'''
		dataDict = MessageHandler.DataToDict(self.cfile)
		self.saveDataToFile( TMP_FOLDER + "theworm.zip", dataDict["Payload:"])
		self.runCode()
		print "Got data, unziped it and made it run"
	
	def runCode(self):
		'''
		Unzips the reseved files, and runs the default segment code
		'''
		global NumberOfWormsStarted
		NumberOfWormsStarted += 1
		self.setNumberOfStartedSegmets(NumberOfWormsStarted)
		print "Starting next worm nr: ", NumberOfWormsStarted
		os.makedirs(TMP_FOLDER + str(NumberOfWormsStarted))
		res, text = commands.getstatusoutput( "unzip -o "+ TMP_FOLDER +"theworm.zip -d " + TMP_FOLDER + str(NumberOfWormsStarted) )
		res, text = commands.getstatusoutput("python "+ TMP_FOLDER + str(NumberOfWormsStarted) + "/cells.py")
		
			
		
	def saveDataToFile(self, filename, data):
		'''
		saves the given data to the given filename
		'''
		try:
			new_file = open(filename, 'wb')
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
		FileClient.sendFile("theworm.zip", TARGET_IPS[random.randint(0, len(TARGET_IPS) - 1)] , WORM_GATE_PORT)
	else:
		print "Starting Server test"
		server = FileServer(LISTEN_PORT, WORM_GATE_PORT)
		server.main()
