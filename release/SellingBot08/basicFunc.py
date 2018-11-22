#basicFunc.py
#Autor: Leon Breidt
#07.11.2018

import time
from pynput.keyboard import Key, Controller, KeyCode
import pynput._util.win32_vks as VK

def output(out):
    print(out)
    a = open('./logfile.txt', 'a+')
    a.write(str(out))
    a.close()

def isReceivedItemAvailable(INVENTORY, ItemName):
    if ItemName not in INVENTORY:
        return False

    for ele in INVENTORY[ItemName]:
        if ele[0] > 0:
            return True
    return False

def getDropKey():
    drop = input("Welche Taste wird als Drop-Taste benutzt: ")
    if drop == "LeftShift":
        return Key.shift_l
    return drop

def getAfkMessage():
    print("Welche Nachricht soll dem Kunden angezeigt werden, wenn er eine Nachricht an den Bot schreibt?")
    Message = input("(Leer lassen, wenn keine Nachricht angezeigt werden soll) :")
    return Message


def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def getItemByPrice(SELLING, amount):
    for key in SELLING:
        if amount == key:
            return SELLING[key]
    return False

def quickSay(keyboard, message):
    output(message)
    keyboard.press('t')
    time.sleep(0.1)
    keyboard.release('t')
    keyboard.type(message)
    time.sleep(0.2)
    keyboard.press(KeyCode.from_vk(VK.RETURN))
    time.sleep(0.1)
    keyboard.release(KeyCode.from_vk(VK.RETURN))
