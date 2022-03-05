import requests, json

# oldPossibleChars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
possibleChars = ["_", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

totalChecked = 0
currentNames = []
unclaimedNames = []

def requestMC(nameList):
    r = requests.post('https://api.mojang.com/profiles/minecraft', json=nameList)
    return json.loads(r.text)


def checkingFunction(name):
    global totalChecked, currentLoop, susName
    
    if len(currentNames) == 10:

        response = requestMC(currentNames)

        if len(response) != 10:
            for susName in currentNames:

                indResponse = requestMC([susName])

                if len(indResponse) == 0:
                    unclaimedNames.append(susName)
                    print("Found Name: " + susName)
            
            currentNames.clear()
            currentNames.append(name)
        else:
            currentNames.clear()
            currentNames.append(name)

    else:
        currentNames.append(name)

    totalChecked = totalChecked + 1
    print("Total Checked: " + str(totalChecked)) # Comment this line to only see found names

for firstChar in possibleChars:
    for secondChar in possibleChars:
        for thirdChar in possibleChars:
            checkingFunction(firstChar + secondChar + thirdChar)
