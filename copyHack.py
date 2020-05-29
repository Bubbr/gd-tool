import gdmt
import verifyHack
import json

prefer = json.load(open('Game.json', 'r'))['prefer']['hax']['copyHack']

if __name__ == "__main__":
    print(f'Bienvenido de vuelta {gdmt.playerName}!')
    lvl = gdmt.Level(byName=input("Introduce el nombre o id del nivel a copiar!\n> "))
    new_lvl = {
        "kCEK":4,
        "k2":lvl.name,
        "k3":lvl.desc64,
        "k4":lvl.compressedString,
        "k5":gdmt.playerName,
        "k13":True,
        "k16":1,
        "k21":2,
        "k45":lvl.musicId,
        "k50":34,
        "kI6":{}
    }
    key = f'k_{gdmt.getLastLevel()+1}'
    gdmt.updatePlist(gdmt.localLevels["LLM_01"], [key], [new_lvl])

    if prefer["auto-verify"]:
        verifyHack.verify(key)

    gdmt.saveDat()
    gdmt.local.encrypt()