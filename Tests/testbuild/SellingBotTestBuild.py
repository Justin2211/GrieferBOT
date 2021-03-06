#Minecraft-Sprache: Deutsch

##    GrieferBOT - Ein einfacher Verkaufsbot für Griefergames.net
##    Copyright (C) 2018  LocutusV0nB0rg
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.

warranty = """    GrieferBOT  Copyright (C) 2018  LocutusV0nB0rg

    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
    """

import time, os, re, datetime
from pynput.keyboard import Key, Controller, KeyCode
import pynput._util.win32_vks as VK

keyboard = Controller()

SELLING = dict() #{1100:'beacon', 333:'Skull'}
INVENTORY = dict() #{'beacon':[(21, '1'), (41, '3')], 'Skull':[(42, '2')]}

def output(out):
    print(out)
    out += '\n'
    a = open('./logfile.txt', 'a+')
    a.write(out)
    a.close()
    

def push(key):
    keyboard.press(key)
    keyboard.release(key)

def sayInChat(message):
    output(message)
    output('')
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
    global INVENTORY

    for thing in INVENTORY:
        if thing == item:
            for ele in INVENTORY[item]:
                if ele[0]>0:
                    push(ele[1])
                    time.sleep(0.15)
                    push('q')
                    ele[0] -= 1
                    confirm = 'Dropped ' + item
                    output(confirm)
                    return

def isReceivedItemAvailable(ItemName):
    global INVENTORY
    if ItemName not in INVENTORY:
        return False

    for ele in INVENTORY[ItemName]:
        if ele[0] > 0:
            return True
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

def getInv():
    global INVENTORY, SELLING
    i=0
    while i<10:
        i+=1
        strin = 'Name des Items auf Slot ' + str(i) + ': '
        item = input(strin)

        if item == '':
            return False

        number = int(input('Wieviele Items sollen verkauft werden: '))
        preis = int(input('Wieviel soll ein Item kosten: '))

        if item not in INVENTORY:
            INVENTORY[item] = [[number, str(i)]]
        else:
            INVENTORY[item].append([number, str(i)])

        SELLING[preis] = item
        

if __name__ == '__main__':
    print(warranty)

    getInv()
    output('[+] Bestand zu Beginn des Durchlaufes')
    output(str(INVENTORY))
    output(str(SELLING))
    output('[+] Bereit für Kunden.')
    
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

                now = datetime.datetime.now()
                strings = '[o] [' + now.strftime("%Y-%m-%d %H:%M") + '] Spieler: ' + name + ' | Betrag: ' + liste[5]
                output(strings)

                pre = liste[5][1:]

                pre = re.sub(',', '', pre)
                        

                diff = float(pre)
                item = getItemByPrice(diff)

                print(item)

                if not item:
                   payPlayerAmount(name, diff)
                   sayInChat('/msg ' + name + ' Tut mir leid, aber ein Item mit diesem Preis scheint es nicht zu geben!')
                else: 
                    if isReceivedItemAvailable(item):
                        dropItem(item)
                        sayInChat('/msg ' + name + ' Danke für ihren Einkauf!')
                    else:
                        payPlayerAmount(name, diff)
                        sayInChat('/msg '+ name + ' Dieses Item ist leider ausverkauft. Hier hast du dein Money wieder!')

                
                
        
        
