from urllib.request import urlopen, Request
import base64
import localdat as local
from xml.dom import minidom
import json
import plistlib as plib
import gzip

url = "http://www.boomlings.com"
stuff = "gameVersion=21&binaryVersion=34&gdw=0"
download = "/database/downloadGJLevel22.php"
search = "/database/getGJLevels21.php"
user = "/database/getGJUsers20.php"
userinfo = "/database/getGJUserInfo20.php"
usercomments = "/database/getGJAccountComments20.php"
levelcomments = "/database/getGJComments21.php"
secret = "Wmfd2893gb7"

def fixPlist(file_name, output_name):
    with open(file_name, 'r') as f:
        s = f.read()
        s = s.replace('<k>','<key>')
        s = s.replace('</k>','</key>')
        s = s.replace('<s>','<string>')
        s = s.replace('</s>','</string>')
        s = s.replace('<d>','<dict>')
        s = s.replace('</d>','</dict>')
        s = s.replace('<a>','<array>')
        s = s.replace('</a>','</array>')
        s = s.replace('<i>','<integer>')
        s = s.replace('</i>','</integer>')
        s = s.replace('<r>','<real>')
        s = s.replace('</r>','</real>')
        s = s.replace('<t/>','<true/>')
        s = s.replace('<f/>','<false/>')
        s = s.replace('<d/>','<data></data>')
        open(output_name, 'w').write(s)
        f.close()

def readPlist(file_name):
    with open(file_name, 'rb') as f:
        p = plib.load(f)
        f.close()
        return p

def hasLocalDat():
    try:
        open('CCGameManager.dat.xml')
        open('CCLocalLevels.dat.xml')
        open('CCGameManager.plist')
        open('CCLocalLevels.plist')
        return True
    except IOError:
        return False

if hasLocalDat():
    localLevels = readPlist('CCLocalLevels.plist')
    localData = readPlist('CCGameManager.plist')
else:
    print('Preparando todo, esto solo se ejecutará una vez...')
    local.decrypt()
    fixPlist('CCLocalLevels.dat.xml', 'CCLocalLevels.plist')
    fixPlist('CCGameManager.dat.xml', 'CCGameManager.plist')
    localLevels = readPlist('CCLocalLevels.plist')
    localData = readPlist('CCGameManager.plist')
    print('Listo!')

playerUDID = localData['playerUDID']
playerName = localData['playerName']
playerUserID = localData['playerUserID']

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
        self.creator = User(s[11])
        self.decompressedString = self.decompress(self.compressedString)
    
    def decompress(self, raw):
        raw = list(raw)
        raw[12] = "/"
        raw = "".join(raw)
        raw = raw.replace('-', '+')
        raw = raw.replace('_', '/')
        return gzip.decompress(base64.b64decode(raw))
    
    def saveRaw(self):
        with open(f'./output/{self.id} - {self.name}.txt', 'w') as file:
            file.write(self.raw)
            file.close()

    def saveAsJSON(self):
        with open(f'./output/{self.id} - {self.name}.json', 'w') as file:
            data = {
                'id':self.id,
                'name':self.name,
                'creator':self.creator.name,
                'level_string':self.compressedString
                }
            json.dump(data, file)
            file.close()

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
    p = f"{stuff}&udid={playerUDID}&uuid={playerUserID}&targetAccountID={d}&secret={secret}"
    return getFromUrl(userinfo, p)

def getLevelComments(page, Id):
    p = f"{stuff}&page={page}&total=0&secret={secret}&mode=0&levelID={Id}"
    return getFromUrl(levelcomments, p)

def getGridPos(pos):
    return (pos[0]/30+0.5, pos[1]/30-0.5)

def printData(raw):
    data = raw.split(';')
    data = data[1:]
    for i in range(0, len(data)):
        print(data[i])
