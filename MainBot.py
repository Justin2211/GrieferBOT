#Minecraft-Sprache: Deutsch

import time, os

PositionOfBot=[100, 100, 0]

helperb = 0

BALANCE = 0
PRICES = {'beacon':800, 'dragon_egg':1800, 'diamond': 3}
SELLING = {1000:'beacon', 2000:'dragon_egg', 5:'diamond'}
INVENTORY = {'beacon': 5, 'dragon_egg': 4, 'diamond': 20}

def getLastChatLine():
    return 'LastLine'

def sayInChat(string):
    print('-> ' + string)

def dropItemAtPosition(pos, item, amount):
    global INVENTORY
    INVENTORY[item] -= amount
    print('dropped', item, 'at', pos, 'Number:', amount)

def getPlayerName(x, y, z):
    if isPlayerAtRelativePosition(x, y, z):
        return 'Steve'
    else:
        return False

def payPlayerAmount(name, amount):
    global BALANCE
    string = '/pay ' + str(name) + ' ' + str(amount)
    BALANCE -= amount
    sayInChat(string)

def isReceivedItemAvailable(ItemName):
    global INVENTORY
    if INVENTORY[ItemName]>0:
        return True
    else:
        return False

def getPriceOfItem(ItemName):
    return PRICES[ItemName]

def getItemByPrice(amount):
    for key in SELLING:
        if amount == key:
            return SELLING[key]
    return False

def turn90clockwise():
    pass

def checkBalance():
    global helperb
    return helperb

def outgoing():
    pass

def incoming():
    global BALANCE, helperb
    currentBalance = checkBalance()
    if BALANCE < currentBalance:
        diff = currentBalance - BALANCE
        BALANCE = currentBalance
        item = getItemByPrice(diff)
        name = getPlayerName(5, 0, 0)
        if not name:
            sayInChat('Please do not pay me money when you are not in a trading room. I cannot return the money since I do not know whose money it is.')
        else:
            if not item:
               payPlayerAmount(name, diff)
               sayInChat('/msg ' + name + ' I am sorry, but I cannot find an item with that price. Please try another amount.')
            else:
                if isReceivedItemAvailable(item):
                    dropItemAtPosition(1, item, 1)
                else:
                    payPlayerAmount(name, diff)
                    sayInChat('/msg '+ name + ' I am sorry, but the Item you wanted to purchase is sold out. Here, take your money back!')

    helperb = BALANCE
        
def mainloop():
    incoming()
    outgoing()
    BALANCE = checkBalance()
    time.sleep(0.05) #Best case gives you 20 TPS, so 1/20 is the loop Speed

def waitforaction():
    global helperb, BALANCE
    inp = input('> ')
    if inp == '':
        return
    else:
        if str(list(inp)[:8])==str(list('/pay bot')):
            hels = ''
            for ele in list(inp)[9:]:
                hels += ele
            helperb += int(hels)
        elif inp == '/money':
            print('Money:', BALANCE)
        
            

if __name__ == '__main__':
    helperb = checkBalance()
    BALANCE = checkBalance()
    while True:
        waitforaction()
        mainloop()

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == "__main__":
    logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r")
    loglines = follow(logfile)
    for line in loglines:
        if "[Client thread/INFO]: [CHAT]" in line:
            message = line[40:]
            liste = message.split(' ')
            liste.append("-")
            liste.append("-")
            liste.append("-")
            if liste[3] == 'hat' or liste[3] == 'hat\n':#2tes nur für lokal
                joining = ''
                for ele in liste:
                    joining += ele
                    joining += ' '
                print('Spieler:', liste[2])
                print('Betrag:', liste[5])
                

        
