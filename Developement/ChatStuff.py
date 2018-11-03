from pynput.keyboard import Key, Controller, KeyCode
import pynput._util.win32_vks as VK
import time

class ChatHandler(object):
    def __init__(self, controller, SLOWCHAT):
        self.slowchat = SLOWCHAT
        self.controller = controller

    def updateSlowchat(self, newSlowchat):
        self.slowchat = newSlowchat

    def toggleSlowchat(self):
        self.slowchat = not self.slowchat

    def msg(self, player, message):
        self.sayInChat("/msg " + player + " " + message)

    def push(self, key):
        self.controller.press(key)
        self.controller.release(key)

    def quickSay(self, message):
        self.controller.press('t')
        time.sleep(0.05)
        self.controller.release('t')
        self.controller.type(message)
        time.sleep(0.1)
        self.controller.press(KeyCode.from_vk(VK.RETURN))
        time.sleep(0.05)
        self.controller.release(KeyCode.from_vk(VK.RETURN))

    def sayInChat(self, message):
        self.controller.press('t')
        time.sleep(0.1)
        self.controller.release('t')
        self.controller.type(message)
        time.sleep(0.2)
        self.controller.press(KeyCode.from_vk(VK.RETURN))
        time.sleep(0.1)
        self.controller.release(KeyCode.from_vk(VK.RETURN))
        if self.slowchat:
            time.sleep(3.05)
        else:
            time.sleep(1.05)
