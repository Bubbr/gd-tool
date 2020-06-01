import gdmt

def verify(lvl_k):
    gdmt.updatePlist(gdmt.localLevels["LLM_01"][lvl_k], ["k14", "k19", "k71"], [True, 100, 100])

if __name__ == "__main__":
    lvl_name = input('Nombre del nivel:\n> ')
    lvl_key = gdmt.getLevelKey(lvl_name)

    if lvl_key:
        verify(lvl_key)
        gdmt.saveDat()
        gdmt.local.encrypt()
    else:
        print("Ese nivel al parecer no te pertenece :/. ¿Lo escribiste bien?")