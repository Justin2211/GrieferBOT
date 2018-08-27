#Minecraft-Sprache: Deutsch

import time, os
from pynput.keyboard import Key, Controller, KeyCode
import pynput._util.win32_vks as VK

keyboard = Controller()

SELLING = {1000:'beacon', 2000:'dragon_egg', 333:'Skull'}
INVENTORY = {'beacon': 64, 'dragon_egg': 64, 'Skull':64}

def push(key):
    keyboard.press(key)
    keyboard.release(key)

def sayInChat(message):
    keyboard.press('t')
    time.sleep(0.1)
    keyboard.release('t')
    keyboard.type(message)

    keyboard.press(KeyCode.from_vk(VK.RETURN))
    time.sleep(0.1)
    keyboard.release(KeyCode.from_vk(VK.RETURN))
    

def dropItem(item):
    if item == 'beacon':
        push('1')
        time.sleep(0.05)
        push('q')
    elif item == 'dragon_egg':
        push('2')
        time.sleep(0.05)
        push('q')
    elif item == 'Skull':
        push('3')
        time.sleep(0.05)
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
            if liste[3] == 'hat':
                strings = 'Spieler: ' + liste[2] + ' | Betrag: ' + liste[5] + '\n'
                print(strings)

                a = open('./logfile.txt', 'a+')
                a.write(strings)
                a.close()

                diff = int(liste[5][1:])
                item = getItemByPrice(diff)
                dropItem(item)
                sayInChat('/msg ' + liste[2] + ' Danke für ihren Einkauf!')
                
        
        
