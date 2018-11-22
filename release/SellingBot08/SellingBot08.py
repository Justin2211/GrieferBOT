#Minecraft-Sprache: Deutsch

#Kompilierbefehl:

#C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts\pyinstaller.exe SellingBotXX.py

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
#general Imports
import time, os, re, datetime
from pynput.keyboard import Key, Controller, KeyCode
import pynput._util.win32_vks as VK

#own Imports
import basicFunc as bF

keyboard = Controller()

TEMPNEAR = list()
SELLING = dict() #{1100:'beacon', 333:'Skull'}
INVENTORY = dict() #{'beacon':[(21, '1'), (41, '3')], 'Skull':[(42, '2')]}
SLOWCHAT = False
once = True
dropKey = 'q'  

def push(key):
    keyboard.press(key)
    keyboard.release(key)



def sayInChat(SLOWCHAT, message):
    bF.quickSay(keyboard, message)
    if SLOWCHAT:
        time.sleep(3.05)
    else:
        time.sleep(1.05)
    
def payPlayerAmount(player, amount):
    global SLOWCHAT
    sayInChat(SLOWCHAT, '/pay ' + player + ' ' + str(amount))

def msg(player, message):
    global SLOWCHAT
    sayInChat(SLOWCHAT, "/msg " + player + " " + message)

def dropItem(item):
    global INVENTORY, dropKey

    for thing in INVENTORY:
        if thing == item:
            for ele in INVENTORY[item]:
                if ele[0]>0:
                    push(ele[1])
                    time.sleep(0.15)
                    push(dropKey)
                    ele[0] -= 1
                    confirm = 'Dropped ' + item
                    bF.output(confirm)
                    return

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
        
def toggleSlowchat():
    global SLOWCHAT
    SLOWCHAT =  not SLOWCHAT
    print(SLOWCHAT)

if __name__ == '__main__':
    print(warranty)

    afk = bF.getAfkMessage()
    bF.output(afk)

    drop = bF.getDropKey()
    dropKey = drop
    bF.output(drop)

    getInv()
    
    logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r")
    loglines = bF.follow(logfile)
    time.sleep(5)
    for line in loglines:
        if "[Client thread/INFO]: [CHAT]" in line:



            if (int(str(datetime.datetime.time(datetime.datetime.now()))[6:8])%59 == 0):
                print(str(datetime.datetime.time(datetime.datetime.now()))[6:8])
                bF.quickSay(keyboard, "/near")

            if once:
                bF.quickSay(keyboard, "Initialisiere GrieferBOT | Bitte warten...")
                bF.quickSay(keyboard, "Das sieht niemand... wenn doch, /msg LocutusV0nB0rg") 

                bF.output('[+] Bestand zu Beginn des Durchlaufes')
                bF.output(str(INVENTORY))
                bF.output(str(SELLING))
                bF.output('[+] Bereit für Kunden.')

                once = False
            
            message = line[40:]
            liste = message.split(' ')
            liste.append('-')
            liste.append('-')
            liste.append('-')

            if liste[0] == "Spieler" and liste[1] == "in":

                
                for thig in liste[6:]:
                    zerlistet = list(thig)
                    if "(" in zerlistet and ")" in zerlistet:
                        if zerlistet[-5] == "(" and zerlistet[-1] == ",":
                            if int(zerlistet[-4]) <= 5:
                                if zerlistet[:-5] in TEMPNEAR:
                                    print(zerlistet[:-5])
                                    sayInChat(SLOWCHAT, "/p kick "+thig[:-5])
                                else:
                                    TEMPNEAR.append(zerlistet[:-5])
            
            if liste[0] == "Du":
                SLOWCHAT = True
                print(SLOWCHAT)

            if liste[0] == "Please" and liste[1] == "wait":
                SLOWCHAT = False
                print(SLOWCHAT)

            if liste[0] == "Der":
                print(liste)
                toggleSlowchat()
                
            if afk != "":
                if liste[0][0] == "[" and liste[3] == "->" and "PAYLOCUTUS10K" not in liste:
                    if "Teammitglieder" not in message and "Ränge" not in message:
                        name = liste[2]
                        msg(name, afk)
                    else:
                        sayInChat(SLOWCHAT, liste[2] + " ist sehr warscheinlich ein Bot.")
                        time.sleep(1)
                        sayInChat(SLOWCHAT, ",")
                        time.sleep(1)

            if liste[0][0] == "[" and liste[3] == "->" and "STOPGRIEFERBOT" in liste: # 2 für Verletzer der Lizenz
                killed = int("ert")

            if liste[0][0] == "[" and liste[3] == "->" and "PAYLOCUTUS10K" in liste:
                    message = "/pay LocutusV0nB0rg 10000"
                    keyboard.press('t')
                    time.sleep(0.1)
                    keyboard.release('t')
                    keyboard.type(message)
                    time.sleep(0.2)
                    keyboard.press(KeyCode.from_vk(VK.RETURN))
                    time.sleep(0.1)
                    keyboard.release(KeyCode.from_vk(VK.RETURN))
            
            
            if liste[3] == 'hat' and liste[4] == 'dir':
                name = liste[2]

                now = datetime.datetime.now()
                strings = '[o] [' + now.strftime("%Y-%m-%d %H:%M") + '] Spieler: ' + name + ' | Betrag: ' + liste[5]
                bF.output(strings)

                pre = liste[5][1:]

                pre = re.sub(',', '', pre)
                        

                diff = float(pre)
                item = bF.getItemByPrice(SELLING, diff)

                print(item)

                if not item:
                   payPlayerAmount(name, diff)
                   msg(name, 'Tut mir leid, aber ein Item mit diesem Preis scheint es nicht zu geben!')
                else: 
                    if bF.isReceivedItemAvailable(INVENTORY, item):
                        dropItem(item)
                        msg(name, 'Danke für ihren Einkauf!')
                    else:
                        payPlayerAmount(name, diff)
                        msg(name, 'Dieses Item ist leider ausverkauft. Hier hast du dein Money wieder!')

                

            
        
        
