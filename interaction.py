from pynput.keyboard import Key, Controller
import time

def push(key):
    keyboard.press(key)
    keyboard.release(key)

time.sleep(5)

keyboard = Controller()

push('q')
