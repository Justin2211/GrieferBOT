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

    This is Expert Mode. Wenn du nicht genau weisst was du hier tust, kann
    das großen finanziellen Schaden auf GrieferGames bedeuten!
    """

import time, os, re, datetime
from pynput.keyboard import Key, Controller, KeyCode
import pynput._util.win32_vks as VK
from ChatStuff import ChatHandler

keyboard = Controller()
mouse = Controller()

Admins = ["LocutusV0nB0rg"]
SELLING = dict() #{1100:'beacon', 333:'Skull'}
INVENTORY = dict() #{'beacon':[(21, '1'), (41, '3')], 'Skull':[(42, '2')]}
SLOWCHAT = False
once = True
Ranksandsep = ["Spieler", "Ultra", "YouTuber", "Freund", "Freund+", "Premium", "Griefer", "Titan", "Legende", "Champ", "|"]
SellingRooms = {"LeftRoom":"", "RightRoom":""}
turned = "left"
dropKey = None

def output(out):
    print(out)
    out += '\n'
    a = open('./logfile.txt', 'a+')
    a.write(out)
    a.close()    
  
def payPlayerAmount(player, amount):
    global chat
    chat.sayInChat('/pay ' + player + ' ' + str(amount))

def dropItem(item):
    global INVENTORY, dropKey

    for thing in INVENTORY:
        if thing == item:
            for ele in INVENTORY[item]:
                if ele[0]>0:
                    chat.push(ele[1])
                    time.sleep(0.15)
                    push(dropKey)
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
        
def getAfkMessage():
    print("Welche Nachricht soll dem Kunden angezeigt werden, wenn er eine Nachricht an den Bot schreibt?")
    Message = input("(Leer lassen, wenn keine Nachricht angezeigt werden soll) :")
    return Message

def toggleSlowchat():
    global SLOWCHAT
    SLOWCHAT =  not SLOWCHAT
    print(SLOWCHAT)

def turnLeft():
    global mouse, turned
    if turned != "left":
        mouse.move(-1000, 0)
    turned = "left"
    
def turnRight():
    global mouse, turned
    if turned != "right":
        mouse.move(1000, 0)
    turned = "right"

def getDropKey():
    global dropKey
    opfile = open(os.getenv("APPDATA")+"/.minecraft/options.txt", "r")
    for line in opfile:
        if "key_key.drop" in line:
            liste = line.split('.')
            print(liste)
            dropKey = liste[-1].split(":")[-1]
            print(dropKey)
            return getKeyByCode(int(dropKey))


def getKeyByCode(code):
    keyfile = open("./KeyCodes.txt", "r")
    werk =  dict()
    for line in keyfile:
        a = re.sub('\t', '', line)
        b = re.sub('\n', '', a)
        c = a.split(' ')
        c[-1] = re.sub('\n', '', c[-1])
        print(c)
        if int(c[0]) == code:
            print(c[-1])
            return c[-1].lower()

if __name__ == '__main__':
    chat = ChatHandler(keyboard, SLOWCHAT)
    
    print(warranty)

    afk = getAfkMessage()
    output(afk)

    getInv()
    dropKey = getDropKey()
    
    logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r")
    loglines = follow(logfile)
    time.sleep(5)
    for line in loglines:
        if "[Client thread/INFO]: [CHAT]" in line:

            if once:
                chat.quickSay("Initialisiere GrieferBOT | Bitte warten...")
                chat.quickSay("Das sieht niemand... wenn doch, /msg LocutusV0nB0rg") 

                output('[+] Bestand zu Beginn des Durchlaufes')
                output(str(INVENTORY))
                output(str(SELLING))
                output('[+] Bereit für Kunden.')

                once = False
            
            message = line[40:]
            liste = message.split(' ')
            liste.append('-')
            liste.append('-')
            liste.append('-')
            ########
            if liste[0] == "Du":
                chat.updateSlowchat(True)
                print(SLOWCHAT)
            ########
            if liste[0] == "Please" and liste[1] == "wait":
                chat.updateSlowchat(False)
                print(SLOWCHAT)
            ########
            if liste[0] == "Der" and (liste[7] == "verlangsamt" or liste[7]=="auf") :
                print(liste)
                chat.toggleSlowchat()
            ########  
            if afk != "":
                if liste[0][0] == "[" and liste[3] == "->":
                    if "Teammitglieder" not in message and "Ränge" not in message:
                        output(message)
                        name = liste[2]
                        print(name)
                        chat.msg(name, afk)
                    else:
                        chat.sayInChat(liste[2] + " ist sehr warscheinlich ein Bot.")
                        time.sleep(1)
                        chat.sayInChat(",")
                        time.sleep(1)
            #######
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
                   chat.msg(name, 'Tut mir leid, aber ein Item mit diesem Preis scheint es nicht zu geben!')
                else: 
                    if isReceivedItemAvailable(item):
##                        if SellingRooms["LeftRoom"] == name:
##                            #turnLeft()
##                            dropItem(item)
##                            msg(name, 'Danke für ihren Einkauf!')
##                        elif SellingRooms["RightRoom"] == name:
##                            #turnRight()
                            dropItem(item)
                            chat.msg(name, 'Danke für ihren Einkauf!')
##                        else:
##                            payPlayerAmount(name, diff)
##                            msg(name, 'Bitte begebe dich zuerst in eine der Kaufkammern.')
                    else:
                        payPlayerAmount(name, diff)
                        chat.msg(name, 'Dieses Item ist leider ausverkauft. Hier hast du dein Money wieder!')
            #######
            now = datetime.datetime.now()
            
            if int(now.strftime("%S"))%5==0 and liste[0][1:7] != "???????" :
                SetNear(True)
                chat.quickSay("/near")
                        
##            if liste[1] == "in" and liste[3] == "Nähe:":
##                data = liste [4:]
##                for ele in data:
##                    if ele not in Ranksandsep and len(ele)>6:
##                        try:
##                            int(ele[-5])
##                        except:
##                            name = ele[:-5]
##                            distance = int(ele[-4])
##                            print(name, distance)
##                            if distance <= 3:
##                                sayInChat("/p kick " + name)
##                            if distance == 4:
##                                SellingRooms["RightRoom"] = name
##                            if distance == 5:
##                                SellingRooms["LeftRoom"] = name                            
                

            
        
        
