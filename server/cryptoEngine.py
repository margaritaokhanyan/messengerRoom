from cryptography.fernet import Fernet
import base64
import rsa

class AESCrypto:
    def __init__(self, key):
        self.mainKey = key
        self.fernet = Fernet(key)

    def AESGetKey(self):
        return self.mainKey

    def AESEncrypt(self, rawData):
        return self.fernet.encrypt(rawData)

    def AESDecrypt(self, cipher):
        return self.fernet.decrypt(cipher)

    def AESGenerateKey():
        return Fernet.generate_key()

class RSACrypto:
    publicKey = rsa.key.PublicKey
    privateKey = rsa.key.PrivateKey
    trustCertificate = b'2ed17da8-34f4-4263-9aeb-d7378db98f68' # hardcoded certificate TODO

    def RSAAutoConfig(self):
        self.publicKey, self.privateKey = self.RSAGenerateKeys()
        ff = self.publicKey.save_pkcs1()
        print(ff)
        self.publicKey.load_pkcs1(ff)

    def RSASetKeys(self, pubKey, privKey):
        self.publicKey = pubKey
        self.privateKey = privKey

    def RSAGetPublicKey(self):
        return self.publicKey.save_pkcs1()

    def RSAEncrypt(self, rawData, key):
        return rsa.encrypt(rawData, key)

    def RSADecrypt(self, cipher):
        try:
            return rsa.decrypt(cipher, self.privateKey)
        except:
            return False

    def RSAGenerateKeys(self):
        return rsa.newkeys(2048)

    def RSAValidateTrustCertificate(self, data):
        tmp = self.RSADecrypt(data)
        print("Exac Certificate : ", tmp)
        if tmp == self.trustCertificate:
            return True
        return False


# rsaCrypto = RSACrypto()
# pubKey, privKey = rsaCrypto.RSAGenerateKeys()
# rsaCrypto.RSASetKeys(pubKey, privKey)
# cipher = rsaCrypto.RSAEncrypt("The quick brown fox jumps over the lazy dog".encode('utf-8'))
# rawText = rsaCrypto.RSADecrypt(cipher)
# print(cipher)
# print(rawText)


# key = AESCrypto.AESGenerateKey()
# aesCrypto = AESCrypto(key)
# cipher = aesCrypto.AESEncrypt("The quick brown fox jumps over the lazy dog".encode('utf-8'))
# rawText = aesCrypto.AESDecrypt(cipher)
# print(cipher)
# print(rawText)
# print(type(key))