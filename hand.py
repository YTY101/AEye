import time
import pyautogui
from pynput.mouse import Button, Listener, Controller
import ctypes
import pydirectinput

class Hand:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.listener = Listener(on_click=self.on_click)
        self.mouse = Controller()
        
    def work(self):
        self.listener.start()
    
    def set_target(self, x, y):
        self.x = x
        self.y = y
    
    def on_click(self, x, y, button, pressed):
        if button == Button.middle and pressed:
            # pyautogui.moveTo(self.x, self.y, duration=0.1)
            # self.mouse.position = (self.x, self.y)
            ctypes.windll.user32.SetCursorPos(self.x, self.y)
            # pydirectinput.moveTo(self.x, self.y)
            print(f"Trigger: Moving mouse to ({self.x}, {self.y})")
    

