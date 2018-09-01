from pynput.mouse import Button, Controller
import time

time.sleep(1)

mouse = Controller()

# Read pointer position
print('The current pointer position is {0}'.format(
    mouse.position))

time.sleep(1)
mouse.move(1000, 0)

print('The current pointer position is {0}'.format(
    mouse.position))

time.sleep(1)

mouse.move(-1000, 0)


print('The current pointer position is {0}'.format(
    mouse.position))

