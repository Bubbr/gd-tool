def printLevelData(raw):
    data = raw.split(';')
    print("\n\tHeader\n", data[0], "\n\n\tBody")
    data = data[1:]
    for i in range(0, len(data)):
        print(data[i])

def saveLevelData(raw, path):
    data = raw.split(';')
    result = ""
    result += "\tHeader\n" + data[0] + "\n\n\tBody\n"
    data = data[1:]
    for i in range(0, len(data)):
        result += data[i] + "\n"
    with open(path, 'w') as f:
        f.write(result)
        f.close()