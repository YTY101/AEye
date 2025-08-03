import pyautogui
import time
from pynput.keyboard import KeyCode, Listener


def on_press(key):
    if key == KeyCode.from_char('`'):
        pyautogui.move(10, 10)

listener = Listener(on_press=on_press)

listener.start()

while True:
    pass