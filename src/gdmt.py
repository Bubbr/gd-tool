import localdat as local
import api, cripto, util

from xml.dom import minidom
import json, gzip, base64, sys, os
import plistlib as plib
from collections import OrderedDict

meta            = json.load(open('game.json', 'r'))['meta']
game            = json.load(open('game.json', 'r'))['game']
appdata         = meta['appdata'].replace('%', os.getlogin())

'''
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
'''

class Properties:
    # kA13 <int>
    SongOffset = 0
    # kA15 <bool>
    FadeIn = 0
    # kA16 <bool>
    FadeOut = 0
    # kA14
    Guidelines = ""
    # kA6 <int>
    BackgroundTexture  = 0
    # kA7 <int>
    GroundTexture = 0
    # kA17 <int>
    GroundLine = 0
    # kA18 <int>
    Font = 0
    # kS39 <int>
    kS39 = 0
    #kA2 <int>
    StartingGameMode = 0
    #kA3,0,
    StartingSize = 0
    #kA8 <bool>
    DualMode = 0
    # kA4 <int>
    StartingSpeed = 1
    # kA9 <int>
    StartPos = 0
    # kA10 <bool>
    TwoPlayerMode = 0
    # kA11 <bool>
    InversedGravity = 0

class ColorChannel:
    def __init__(self, channelId, red, green, blue):
        self.ChannelId = channelId
        self.Red = red
        self.Green = green
        self.Blue = blue

        self.Blending = 0
        self.Opacity = 1
    

class ColorChannels:
    pass

class Object:
    pass

class Trigger(Object):
    pass

class Level:
    def __init__(self, string=None, params=None):
        self.properties = Properties()
        if string:
            self.string = string
            self.setup()
        else:
            self.string = self.createHeader(params)
            self.setup()
    
    def setup(self):
        print(self.string)

    def createHeader(self, params):
        if params:
            self.properties = params
        header = f",kA13,{self.properties.SongOffset},kA15,{self.properties},kA16,{self.properties},kA14,{self.properties},kA6,{self.properties},kA7,{self.properties},kA17,{self.properties},kA18,{self.properties},kS39,{self.properties},kA2,{self.properties},kA3,{self.properties},kA8,{self.properties},kA4,{self.properties},kA9,{self.properties},kA10,{self.properties},kA11,{self.properties}"
        return 0

    def addObject(self):
        pass

    def removeObject(self):
        pass

    def setProperty(self):
        pass

class LevelInfo:
    def __init__(self, _id=None, _name=None):
        if (_id == None and _name == None):
            print("No id or level name given.")
            return None
        
        if _id:
            self.raw = api.downloadFromId(id)
        if _name and not _id:
            nid = api.getLevelId(_name)
            if nid == "-1":
                self.raw = nid
            else:
                self.raw = api.downloadFromId(nid)
        
        if self.raw == "-1":
            print("El nivel no existe:", _id or _name)
            return None
        
        self.setup()

    def setup(self):
        ham = self.raw.split(':')

        self.id     = ham[ham.index('1')+1]
        self.name   = ham[ham.index('2')+1]
        self.desc64 = ham[ham.index('3')+1]

        if self.desc64:
            self.desc   = base64.b64decode(self.desc64).decode()
        else:
            self.desc64 = None
            self.desc   = None

        self.creatorId      = ham[ham.index('6')+1]
        self.downloads      = ham[ham.index('10')+1]
        self.localMusic     = ham[ham.index('12')+1]
        self.GDversion      = ham[ham.index('13')+1]
        self.likes          = ham[ham.index('14')+1]
        self.duration       = ham[ham.index('15')+1]
        self.stars          = ham[ham.index('18')+1]
        self.onlineMusic    = ham[ham.index('35')+1]
        self.levelpassword  = ham[ham.index('27')+1]

        if self.levelpassword.split('#')[0] == "Aw==":
            self.levelpassword = 0
        elif len(self.levelpassword.split('#')[0]) < 5:
            self.levelpassword = -1
        else:
            self.levelpassword = str(cripto.decodeLevelPass(self.levelpassword.split('#')[0]), 'utf-8')[1:]
    
    def addLevel(self):
        ham = self.raw.split(':')
        string = ham[ham.index('4')+1]
        string = cripto.decodeLevel(string)
        self.level = Level(string)
        
'''
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
'''


if __name__ == "__main__":
    #nivel = LevelInfo(_name=input("Nombre: "))
    nivel = Level(params=[])
