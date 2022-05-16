from cryptoEngine import RSACrypto
from cryptoEngine import AESCrypto
import rsa
import time
import socket, select, string, sys
from six.moves import input as raw_input

class Client:
    username = 'None'
    serverIP = '127.0.0.1'
    serverPort = 5001

    rsaCrypto = RSACrypto()

    def __init__(self):
        self.rsaCrypto.RSAAutoConfig()

    def clientSetUsername(self, name):
        self.username = name

    def clientBlockingReceive(self):
        rList, wList, error_list = select.select([self.sock] , [], [])
        data = self.sock.recv(4096)
        return data

    def clientBlockingReceiveEncrypted(self):
        rList, wList, error_list = select.select([self.sock] , [], [])
        data = self.sock.recv(4096)
        return self.aesCrypto.AESDecrypt(data)

    def clientEventLoop(self):
        data = self.clientBlockingReceiveEncrypted()
        print(data)
        return data

    def clientRegisterCallback(self, method):
        self.dataReceiveCallback = method

    def clientStartConnection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)
        try :
            self.sock.connect((self.serverIP, self.serverPort))
        except Exception as e:
            print("Error while connecting to server", e)
            return False, e
        return True, None

    def clientSendData(self, rawData):
        try:
            self.sock.send(rawData)
        except Exception as e:
            print(e)
            return False, e
        return True, None

    def clientSendEncryptedData(self, rawData):
        try:
            cipher = self.aesCrypto.AESEncrypt(rawData)
            self.sock.send(cipher)
        except Exception as e:
            print(e)
            return False, e
        return True, None

    def clientHandshake(self):
        tmp = self.rsaCrypto.RSAGetPublicKey()
        print ("Client public key --> ", tmp)
        self.clientSendData(tmp)
        serverPubKey = self.clientBlockingReceive()
        print("Server public key --> ", serverPubKey)
        ecnryptedTrustCertificate = self.rsaCrypto.RSAEncrypt(self.rsaCrypto.RSATrustCertificate(), serverPubKey)
        print(ecnryptedTrustCertificate)
        time.sleep(1)
        self.clientSendData(ecnryptedTrustCertificate)
        tmp = self.clientBlockingReceive()
        print("AES Crypto --> ", tmp)
        if tmp == b'Invlaid':
            return False
        else:
            self.aesCrypto = AESCrypto(tmp)

    def clientStopConnection(self):
        self.sock.close()

    def clientSendMessage(self, message):
        self.clientSendEncryptedData(message)