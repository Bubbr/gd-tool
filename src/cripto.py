import base64, gzip

class XORCipher:
    def __init__(self, key):
        self.key = bytes(key.encode())

    def cipher(self, message):
        msgBytes = bytes(message)
        result = []
        for i in range(0, len(msgBytes)):
            result.append(msgBytes[i] ^ self.key[i%len(self.key)])
        return bytes(result)

XOR_LEVEL_PASS = XORCipher("26364")

def decode0(string, algorithm):
    return algorithm.cipher(base64.b64decode(string))

def decodeLevelPass(lvlpass):
    return decode0(lvlpass, XOR_LEVEL_PASS)


def decodeLevel(string):
    string = list(string)
    string[12] = "/"
    string = "".join(string)
    string = string.replace('-', '+')
    string = string.replace('_', '/')
    return gzip.decompress(base64.b64decode(string)).decode()