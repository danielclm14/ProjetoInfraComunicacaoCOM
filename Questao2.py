# -*- coding: utf-8 -*-
import socket

class Package():
	UserName = ''
	Message = ''
	Acknowledge = 0
	SequenceNumber = 0
	CheckSum = 0

def CalculateCheckSum(message):
	CheckSum = 0
	for char in message:
		CheckSum = CheckSum + ord(char)
	return str(CheckSum)

def GetUserName(username):
	return username

def GetAcknowledge():
	return '@#!@!#!@!$!#!#@#!!' + '555'

def GetSequenceNumber():
	return '@#!@!#!@!$!#!#@#!!' + '222'

def GetChecksum(message):
	return '@#!@!#!@!$!#!#@#!!' + CalculateCheckSum(message)

def GetMessage(message):
	return '@#!@!#!@!$!#!#@#!!' + message

def CreateMessage(username):
	message = raw_input('Your message: ')
	return GetUserName(username) + GetAcknowledge() + GetSequenceNumber() + GetChecksum(message) + GetMessage(message)

def SendPackage (client, socket, username):
	socket.sendto(CreateMessage(username), client)

def isCorrupt(rcvdPackage):
	return rcvdPackage.CheckSum != CalculateCheckSum(rcvdPackage.Message)

def TryAgain (socket, client):
	socket.sendto(_ERROR, client)
	return DecodifyMessage(ReceiveMessage(socket))

def DecodifyMessage(rcvdMessage, socket, client):
	rcvdPackage = Package()
	rcvdPackage.UserName, rcvdPackage.Acknowledge, rcvdPackage.SequenceNumber, rcvdPackage.CheckSum, rcvdPackage.Message  = rcvdMessage.split("@#!@!#!@!$!#!#@#!!")

	if isCorrupt(rcvdPackage):
		rcvdPackage = TryAgain (socket, client)
	
	return rcvdPackage

def ReceiveMessage(socket):
	rcvdDatagram, client = socket.recvfrom(1024)
	rcvdPackage = DecodifyMessage(rcvdDatagram, socket, client)
	print  rcvdPackage.UserName, " says: ", rcvdPackage.Message
	return client

def CallServer(username):
	serverPort = 12000
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	serverSocket.bind(('',serverPort))
	while 1:
		print "Typing..."
		client = ReceiveMessage(serverSocket)
		SendPackage(client, serverSocket, username)

	serverSocket.close()

def CallClient(username):
	clientName = ''
	clientPort = 12000
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client = (clientName, clientPort)         
	while 1:		
		SendPackage(client, clientSocket, username)
		ReceiveMessage(clientSocket)

	clientSocket.close()

#Program:
Username = raw_input("What's your name? ")
_ERROR = 'SYSTEM' + GetAcknowledge() + GetSequenceNumber() + GetChecksum('Something went wrong.') + GetMessage('Something went wrong.')
try:
	CallServer(Username)
	
except Exception:
	CallClient(Username)




