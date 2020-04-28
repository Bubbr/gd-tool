from urllib.request import urlopen, Request
import base64

url = "http://www.boomlings.com"
download = "/database/downloadGJLevel22.php"
search = "/database/getGJLevels21.php"
user = "/database/getGJUsers20.php"
secret = "Wmfd2893gb7"

class Level:
    def __init__(self, byId=None, byName=None):
        if byId:
            print(f"Buscando: {byId}")
            self.raw = downloadFromId(byId)
            self.setLevelData(self.raw)
        elif byName:
            print(f"Buscando: {byName}")
            self.raw = downloadFromId(getLevelId(byName))
            self.setLevelData(self.raw)
        print("Listo!")

    def setLevelData(self, s):
        s = s.split(':')
        self.id = s[1]
        self.name = s[3]
        self.description = base64.b64decode(s[5])
        self.compressedString = s[7]
        self.author = User(s[11])

    def saveAsGML(self):
        pass

    def saveAsDat():
        pass

class User:
    def __init__(self, string):
        data = getUserData(string).split(':')
        self.name = data[1]
        self.id = data[3]

def getFromUrl(f, p):
    p = p.encode()
    data = urlopen(f"{url}{f}", p).read().decode()
    return data

def getUserData(string):
        p = f"gameVersion=21&binaryVersion=34&gdw=0&str={string}&total=0&page=0&secret={secret}"
        return getFromUrl(user, p)

def downloadFromId(Id):
        p = f"gameVersion=21&binaryVersion=34&gdw=0&levelID={Id}&inc=0&extras=0&secret={secret}"
        return getFromUrl(download, p)

def getLevelId(Name):
        p = f"gameVersion=21&binaryVersion=34&gdw=0&type=0&str={Name}&diff=-&len=-&page=0&total=0&uncompleted=0&onlyCompleted=0&featured=0&original=0&twoPlayer=0&coins=0&epic=0&secret={secret}"
        return getFromUrl(search, p).split('|')[0].split(':')[1]

def getGridPos(pos):
    return (pos[0]/30+0.5, pos[1]/30-0.5)
def printData(raw):
    data = raw.split(';')
    data = data[1:]
    for i in range(0, len(data)):
        print(data[i])
