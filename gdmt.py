from urllib.request import urlopen, Request
import localdat as local
from xml.dom import minidom
import json, gzip, base64, sys, os
import plistlib as plib
from collections import OrderedDict

meta            = json.load(open('game.json', 'r'))['meta']
game            = json.load(open('game.json', 'r'))['game']
api             = game['api']

url             = api['base']
stuff           = api['default']
download        = api['downloadGJLevel22']
search          = api['getGJLevels21']
user            = api['getGJUsers20']
userinfo        = api['getGJUserInfo20']
usercomments    = api['getGJAccountComments20']
levelcomments   = api['getGJComments21']
songinfo        = api['getGJSongInfo']

secret          = meta["secret"]

appdata         = meta['appdata'].replace('%', os.getlogin())

def Init():
    if not meta["game_dir"]:
        return "Error: No game directory given.", -1
    return "Ok", 0

def saveDat():
    with open('CCLocalLevels.dat.xml', 'wb') as f:
        plib.dump(localLevels, f)
    with open('CCLocalLevels2.dat.xml', 'wb') as f:
        plib.dump(localLevels, f)

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

def updatePlist(base, args, values):
    for i in range(len(args)):
        base[args[i]] = values[i]

def getLastLevel():
    return int(list(localLevels["LLM_01"].keys())[-1][2:])

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
    localLevels     = readPlist('CCLocalLevels.plist')
    localData       = readPlist('CCGameManager.plist')
else:
    print('\tInicializando...\n')
    local.decrypt()
    fixPlist('CCLocalLevels.dat.xml', 'CCLocalLevels.plist')
    fixPlist('CCGameManager.dat.xml', 'CCGameManager.plist')
    localLevels = readPlist('CCLocalLevels.plist')
    localData = readPlist('CCGameManager.plist')
    print('Listo!')

playerUDID = localData['playerUDID']
playerName = localData['playerName']
playerUserID = localData['playerUserID']

class NewLevel:
    def __init__(self, name, string, params):
        pass
    
    def addObject(self, id, params):
        pass

class Level:
    def __init__(self, byId=None, name=None, local=False, plist=None):
        self.err = False
        try:
            if byId and not local:
                self.raw = downloadFromId(byId)
                self.setDataByRaw(self.raw)
            elif name and not local:
                self.raw = downloadFromId(getLevelId(name))
                self.setDataByRaw(self.raw)
            elif local and plist and name:
                self.key = name
                self.setDataByPlist(plist)
        except:
            self.err = True

    def setDataByPlist(self, data):
        self.name = data["k2"]
        try:
            self.desc64 = data["k3"]
            self.description = base64.b64decode(self.desc64)
        except:
            self.desc64 = "N/A".encode()
            self.description = "N/A".encode()
        try:
            self.compressedString = data["k4"]
            self.decompressedString = self.decompress(self.compressedString)
        except:
            self.compressedString = "N/A"
            self.decompressedString = "N/A"
        self.creator = playerName
        try:
            self.rawSong = getSongInfo(data["k45"])
            temp = self.rawSong.split('|')
            url = str(temp[temp.index("~10~")+1])[1:-1]
            url = url.replace("%3A", ":")
            url = url.replace("%2F", "/")
            self.songInfo = {
                "id":int(str(temp[temp.index("1~")+1])[1:-1]),
                "name":str(temp[temp.index("~2~")+1])[1:-1],
                "by":str(temp[temp.index("~4~")+1])[1:-1],
                "Mb":str(temp[temp.index("~5~")+1])[1:-1],
                "url":url,
            }
            self.songInfo["pathname"] = f'{self.songInfo["id"]} - {self.songInfo["name"]}.mp3'
        except:
            self.rawSong = "N/A"
            self.songInfo = {
                "id":0,
                "name":"n/a",
                "by":"n/a",
                "Mb":"n/a",
                "url":"n/a",
            }
        try:
            if data["k23"] == 0:
                self.len = "tiny"
            elif data["k23"] == 1:
                self.len = "short"
            elif data["k23"] == 2:
                self.len = "medium"
            elif data["k23"] == 3:
                self.len = "long"
            elif data["k23"] == 4:
                self.len = "xl"
        except:
            self.len = "tiny"


    def setDataByRaw(self, s):
        s = s.split(':')
        self.id = s[1]
        self.name = s[3]
        self.description = base64.b64decode(s[5])
        self.desc64 = s[5]
        self.compressedString = s[7]
        self.creator = User(s[11])
        self.decompressedString = self.decompress(self.compressedString)
        self.rawSong = getSongInfo(int(s[s.index("35")+1]))
        temp = self.rawSong.split('|')
        url = str(temp[temp.index("~10~")+1])[1:-1]
        url = url.replace("%3A", ":")
        url = url.replace("%2F", "/")
        self.songInfo = {
            "id":int(str(temp[temp.index("1~")+1])[1:-1]),
            "name":str(temp[temp.index("~2~")+1])[1:-1],
            "by":str(temp[temp.index("~4~")+1])[1:-1],
            "Mb":str(temp[temp.index("~5~")+1])[1:-1],
            "url":url,
        }
        self.songInfo["pathname"] = f'{self.songInfo["id"]} - {self.songInfo["name"]}.mp3'

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

def getLocalLevels(_range=None):
    if _range == None:# Todos lo niveles
        levels = []
        data = localLevels["LLM_01"]
        length = len(data)-2
        data = iter(data)
        next(data)
        i = 0
        for level in data:
            levels.append(Level(name=level, local=True, plist=localLevels["LLM_01"][level]))
            print(f"loading {levels[i].name} - {i}/{length} ({int(i/length*100)}%)")
            i-=-1
        return levels
    else:
        pass

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

def getSongInfo(songID):
    p = f"songID={songID}&secret={secret}"
    return getFromUrl(songinfo, p)

def downloadSong(song, outputpath):
    data = urlopen(song["url"]).read()
    with open(f'{outputpath}{song["pathname"]}', "wb") as f:
        f.write(data)

def getLevelKey(name):
    for level in localLevels["LLM_01"]:
        ham = localLevels["LLM_01"][level]
        try:
            if str(name) == ham["k2"]:
                return level
        except:
            pass
    return False

def getGridPos(pos):
    return (pos[0]/30+0.5, pos[1]/30-0.5)

def printData(raw):
    data = raw.split(';')
    data = data[1:]
    for i in range(0, len(data)):
        print(data[i])


if __name__ == "__main__":
    pass
    #mis_niveles = getLocalLevels()