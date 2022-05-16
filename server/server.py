import socket, select, os, sys
from cryptoEngine import RSACrypto
from cryptoEngine import AESCrypto

class Server:
	# Configurations
	MAX_USERS_COUNT = 10
	buffer = 4096
	port = 5001

	# Class variables
	name=""
	record={}
	connected_list = []
	rsaCrypto = RSACrypto()
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __init__(self):
		print("Server going to start")
		print("Generating RSA keys")
		self.rsaCrypto.RSAAutoConfig()
		print("RSA keys generated, Public key --> ", self.rsaCrypto.RSAGetPublicKey())
		aesKey = AESCrypto.AESGenerateKey()
		self.aesCrypto = AESCrypto(aesKey)
		print("AES key generated --> ", aesKey)
		print("Initializing socket mechanism")
		self.server_socket.bind(("127.0.0.1".encode('utf-8'), self.port))
		self.server_socket.listen(self.MAX_USERS_COUNT)
		self.connected_list.append(self.server_socket)
		print("### Server ready to handle requests ###")

	def serverCheckUsernameUniqueness(self, username):
		if username in self.record.values():
			return False
		return True

	def serverRejectNewUserConnection(self, socketFD, address):
		socketFD.send("Username is busy".encode('utf-8'))
		del self.record[address]
		self.connected_list.remove(sockfd)
		socketFD.close()

	def serverAddNewConnection(self, socketFD, address, name):
		self.record[address]=name
		print ("Client (%s, %s) connected" % addr," [",self.record[address],"]")
		socketFD.send("\33[32m\r\33[1m Welcome to chat room. Enter 'exit' anytime to exit\n\33[0m".encode('utf-8'))
		self.sendToAllUsers(sockfd, "\33[32m\33[1m\r "+name.decode('utf-8')+" joined the conversation \n\33[0m")

	def serverBlockingReceive(self, socketFD):
		print("Start listening socket")
		rList,wList,error_sockets = select.select([socketFD],[],[])
		data = socketFD.recv(self.buffer)
		print("Data received", data)
		return data

	def serverPrepareNewConnection(self):
		sockfd, addr = self.server_socket.accept()
		clientPubKey = self.serverBlockingReceive(sockfd)
		print("Received client RSA Public key --> ", clientPubKey)
		sockfd.send(self.rsaCrypto.RSAGetPublicKey())
		self.connected_list.append(sockfd)
		self.record[addr]=""
		tmp = self.serverBlockingReceive(sockfd)
		if self.rsaCrypto.RSAValidateTrustCertificate(tmp):
			print("Certificate is valid")
			sockfd.send(self.aesCrypto.AESGetKey())
			return True
		else:
			print("Invalid certificate")
			sockfd.send(b'Invalid')
			serverRejectNewUserConnection(sockfd, addr)
			return False

	def handleClientDisconnection(self, sock):
		(i,p)=sock.getpeername()
		self.sendToAllUsers(sock, self.record[(i,p)]+" left the conversation unexpectedly\n")
		print ("Client (%s, %s) is offline (error)" % (i,p)," [",self.record[(i,p)],"]\n")
		del self.record[(i,p)]
		self.connected_list.remove(sock)
		sock.close()

	def serverEventLoop(self):
		while 1:
			rList,wList,error_sockets = select.select(self.connected_list,[],[])
			for sock in rList:
				if sock == self.server_socket:
					self.serverPrepareNewConnection()
				else:
					try:
						data = sock.recv(self.buffer)
						print(data)
						self.sendToAllUsers(sock, data)

					except Exception as e:
						self.handleClientDisconnection(sock)
						continue

	def serverStartConnection(self):
		pass

	def serverSendData(self, rawData):
		pass

	def serverCloseConnection(self):
		self.server_socket.close()

	def serverReceiveUsername(self):
		pass

	def sendToAllUsers (self, sock, message):
		for socket in self.connected_list:
			if socket != self.server_socket and socket != sock :
				try :
					socket.send(message)
				except Exception as e:
					print(e)
					socket.close()
					self.connected_list.remove(socket)


s = Server()
s.serverEventLoop()