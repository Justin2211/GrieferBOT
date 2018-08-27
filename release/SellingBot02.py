#Minecraft-Sprache: Deutsch

import time, os, re
from pynput.keyboard import Key, Controller, KeyCode
import pynput._util.win32_vks as VK

keyboard = Controller()

SELLING = {1100:'beacon', 333:'Skull'}
INVENTORY = {'beacon':21, 'Skull':0}

def push(key):
    keyboard.press(key)
    keyboard.release(key)

def sayInChat(message):
    keyboard.press('t')
    time.sleep(0.1)
    keyboard.release('t')
    keyboard.type(message)
    time.sleep(0.2)
    keyboard.press(KeyCode.from_vk(VK.RETURN))
    time.sleep(0.1)
    keyboard.release(KeyCode.from_vk(VK.RETURN))
    
def payPlayerAmount(player, amount):
    sayInChat('/pay ' + player + ' ' + str(amount))

def dropItem(item):
    if item == 'beacon':
        push('1')
        time.sleep(0.15)
        push('q')
    elif item == 'Skull':
        push('2')
        time.sleep(0.15)
        push('q')
    
    global INVENTORY
    INVENTORY[item] -= 1
    print('dropped', item)

def isReceivedItemAvailable(ItemName):
    global INVENTORY
    if INVENTORY[ItemName]>0:
        return True
    else:
        return False

def getItemByPrice(amount):
    for key in SELLING:
        if amount == key:
            return SELLING[key]
    return False

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r")
    loglines = follow(logfile)

    
    for line in loglines:
        if "[Client thread/INFO]: [CHAT]" in line:
            message = line[40:]
            liste = message.split(' ')
            liste.append('-')
            liste.append('-')
            liste.append('-')
            if liste[3] == 'hat':
                name = liste[2]
                
                strings = 'Spieler: ' + name + ' | Betrag: ' + liste[5] + '\n'
                print(strings)

                a = open('./logfile.txt', 'a+')
                a.write(strings)
                a.close()

                pre = liste[5][1:]

                pre = re.sub(',', '', pre)
                        

                diff = float(pre)
                item = getItemByPrice(diff)

                print(item)

                if not item:
                   payPlayerAmount(name, diff)
                   sayInChat('/msg ' + name + ' I am sorry, but I cannot find an item with that price. Please try another amount.')
                else: 
                    if isReceivedItemAvailable(item):
                        dropItem(item)
                        sayInChat('/msg ' + name + ' Danke für ihren Einkauf!')
                    else:
                        payPlayerAmount(name, diff)
                        sayInChat('/msg '+ name + ' This item is sold out. Here ist your money back!')

                
                
        
        
