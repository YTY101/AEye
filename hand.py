import time
import pyautogui
from pynput.mouse import Button, Listener, Controller
import ctypes
import pydirectinput
import serial

class Hand:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.listener = Listener(on_click=self.on_click)
        self.mouse = Controller()
        self.port = 'COM8'
        self.baudrate = 115200
        self.ser = serial.Serial(self.port, self.baudrate)
        
    def work(self):
        
        self.listener.start()
    
    def set_target(self, x, y):
        self.x = x
        self.y = y
    
    def on_click_sim(self, x, y, button, pressed):
        if button == Button.middle and pressed:
            pyautogui.moveTo(self.x, self.y, duration=0.1)
            # self.mouse.position = (self.x, self.y)
            # ctypes.windll.user32.SetCursorPos(self.x, self.y)
            # pydirectinput.moveTo(self.x, self.y)
            print(f"Trigger: Moving mouse to ({self.x}, {self.y})")

    def on_click(self, x, y, button, pressed):
        if button == Button.middle and pressed:
            # dx, dy = x - self.x, y - self.y
            print(f"Trigger: Moving mouse to ({x}, {y})")
            dx, dy = 30, -30
            command = f"{dx},{dy}\n"
            self.ser.write(command.encode())
            
            
if __name__ == '__main__':
    hand = Hand()
    hand.work()
    while True:
        pass
            
        

