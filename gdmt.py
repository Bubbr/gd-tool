from urllib.request import urlopen, Request
import base64
import localdat as local
from xml.dom import minidom

url = "http://www.boomlings.com"
stuff = "gameVersion=21&binaryVersion=34&gdw=0"
download = "/database/downloadGJLevel22.php"
search = "/database/getGJLevels21.php"
user = "/database/getGJUsers20.php"
userinfo = "/database/getGJUserInfo20.php"
usercomments = "/database/getGJAccountComments20.php"
secret = "Wmfd2893gb7"

def hasLocalDat():
    try:
        open('CCGameManager.dat.xml')
        return True
    except IOError:
        return False

def getUdid():
    return file.getElementsByTagName('s')[26].firstChild.data

def getUuid():
    return file.getElementsByTagName('i')[0].firstChild.data

def getPlayerName():
    return file.getElementsByTagName('s')[27].firstChild.data

if hasLocalDat():
    file = minidom.parse('CCGameManager.dat.xml')
else:
    local.decrypt()
    file = minidom.parse('CCGameManager.dat.xml')

udid = getUdid()
uuid = getUuid()
playername = getPlayerName()

print(f'Sign in as "{playername}"\nudid: {udid}\nuuid: {uuid}')

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
        data = getUserInfo(self.id)
        data = data.split(':')
        self.secretCoins = data[5]
        self.userCoins = data[7]
        self.stars = data[13]
        self.diamonds = data[15]
        self.demons = data[17]

def getFromUrl(f, p):
    p = p.encode()
    data = urlopen(f"{url}{f}", p).read().decode()
    return data

def getUserData(string):
    p = f"{stuff}&str={string}&total=0&page=0&secret={secret}"
    return getFromUrl(user, p)

def downloadFromId(Id):
    p = f"{stuff}&levelID={Id}&inc=0&extras=0&secret={secret}"
    return getFromUrl(download, p)

def getLevelId(Name):
    p = f"{stuff}&type=0&str={Name}&diff=-&len=-&page=0&total=0&uncompleted=0&onlyCompleted=0&featured=0&original=0&twoPlayer=0&coins=0&epic=0&secret={secret}"
    return getFromUrl(search, p).split('|')[0].split(':')[1]

def getUserInfo(string):
    d = getUserData(string).split(':')[21]
    p = f"{stuff}&udid={udid}&uuid={uuid}&targetAccountID={d}&secret={secret}"
    return getFromUrl(userinfo, p)

def getGridPos(pos):
    return (pos[0]/30+0.5, pos[1]/30-0.5)

def printData(raw):
    data = raw.split(';')
    data = data[1:]
    for i in range(0, len(data)):
        print(data[i])
