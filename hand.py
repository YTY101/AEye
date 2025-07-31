import time
import pyautogui
from pynput.mouse import Button, Listener
class Hand:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.listener = Listener(on_click=self.on_click)

    def work(self):
        self.listener.start()
    
    def set_target(self, x, y):
        self.x = x
        self.y = y
    
    def on_click(self, x, y, button, pressed):
        if button == Button.middle and pressed:
            # self.mouse.position(self.x, self.y, duration=0.1)
            pyautogui.moveTo(self.x, self.y, duration=0.1)
            print(f"Trigger: Moving mouse to ({self.x}, {self.y})")
    

