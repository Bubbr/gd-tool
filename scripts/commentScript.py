import gdmt
import base64
import json
import gzip
import io
import plistlib as plib
import localdat

def parseComments(com):
    data = {"comments":[]}
    p = com.split('|')
    for c in p:
        ham = c.split(':')
        bur = ham[0].split('~')
        ger = ham[1].split('~')
        data["comments"].append({
            "userID":bur[bur.index('3')+1],
            "userName":ger[ger.index('1')+1],
            "content":base64.b64decode(bur[bur.index('2')+1]).decode(),
            "percent":bur[bur.index('10')+1]
        })
    return data

def createLevel(data, Id):
    final = ""
    lvl = gdmt.Level(byName=Id)
    deco = lvl.decompressedString.decode()
    a = deco.split(';')
    last = a[-2]
    size = last.split(',')[3]
    for c in data["comments"]:
        x = int(getX(c["percent"], size))
        header = f'{c["userName"]} ({c["percent"]}%)'
        final += f'1,914,2,{x},3,80,32,0.5,31,{base64.b64encode(header.encode()).decode()};'
        final += f'1,914,2,{x},3,65,32,0.5,31,{base64.b64encode(c["content"].encode()).decode()};'
    return f'{deco}{final}'

def encryptLvl(string):
    res = base64.b64encode(gzip.compress(string.encode())).decode()
    res = res.replace('+', '-')
    res = res.replace('/', '_')
    res = f"H4sIAAAAAAAAC{res[13:]}"
    return res

def update(Id, data):
    for lvl in gdmt.localLevels["LLM_01"]:
        if lvl == "_isArr":
            pass
        else:
            ham = gdmt.localLevels["LLM_01"][lvl]
            try:
                if str(ham["k1"]) == str(Id):
                    ham["k4"] = data
                    return ham["k2"]
            except:
                return False

def getX(percent, size):
    return (int(percent)/100)*int(size)

def prettyPrint(raw):
    for c in raw['comments']:
        print(
            f'\n[{c["percent"]}%] {c["userName"]}: {c["content"]}'
        )

if __name__ == "__main__":
    print(f'Bienvenido {gdmt.playerName}!\n')
    od = input('Nivel:\n> ')
    com = parseComments(gdmt.getLevelComments(0, od))
    prettyPrint(com)
    final = createLevel(com, od)
    encrypted = encryptLvl(final)
    res = update(od, encrypted)
    if (res):
        with open(f'./output/{res} - {gdmt.playerName}.txt', 'w') as f:
            f.write(encrypted)
        with open('CCLocalLevels.dat.xml', 'wb') as f:
            plib.dump(gdmt.localLevels, f)
        with open('CCLocalLevels2.dat.xml', 'wb') as f:
            plib.dump(gdmt.localLevels, f)
        localdat.encrypt()
    else:
        print("Ese nivel no te pertenece!")
    input('Preciona enter para salir!')
