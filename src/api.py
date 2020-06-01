from urllib.request import urlopen, Request
import json

api             = json.load(open('game.json', 'r'))['game']['api']

url             = api['base']
stuff           = api['default']
download        = api['downloadGJLevel22']
search          = api['getGJLevels21']
user            = api['getGJUsers20']
userinfo        = api['getGJUserInfo20']
usercomments    = api['getGJAccountComments20']
levelcomments   = api['getGJComments21']
songinfo        = api['getGJSongInfo']
levelpassword   = "/database/getLevelPassword.php"

secret          = json.load(open('game.json', 'r'))['meta']["secret"]

def getFromUrl(f, param):
    param = param.encode()
    data = urlopen(f"{url}{f}", param).read().decode()
    return data

def getUserData(string):
    p = f"{stuff}&str={string}&total=0&page=0&secret={secret}"
    return getFromUrl(user, p)

def downloadFromId(Id):
    p = f"{stuff}&levelID={Id}&inc=0&extras=0&secret={secret}"
    return getFromUrl(download, p)

def getLevelId(Name):
    p = f"{stuff}&type=0&str={Name}&diff=-&len=-&page=0&total=0&uncompleted=0&onlyCompleted=0&featured=0&original=0&twoPlayer=0&coins=0&epic=0&secret={secret}"
    data = getFromUrl(search, p)
    if data == "-1":
        return data
    return data.split('|')[0].split(':')[1]
'''
def getUserInfo(string):
    d = getUserData(string).split(':')[21]
    p = f"{stuff}&udid={playerUDID}&uuid={playerUserID}&targetAccountID={d}&secret={secret}"
    return getFromUrl(userinfo, p)
'''
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