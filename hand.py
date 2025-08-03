import time
import pyautogui
from pynput.mouse import Button, Listener, Controller
from pynput.keyboard import Key, KeyCode, Listener as KeyboardListener
import ctypes
import pydirectinput
import serial

class Hand:
    def __init__(self):
        self.x = -1
        self.y = -1
        # self.listener = Listener(on_click=self.on_click)
        self.listener = KeyboardListener(on_press=self.on_press)
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
            # dx, dy = 30, -30
       
            if self.x != -1 and self.y != -1:
                dx, dy = self.x - x, self.y - y
                # dx, dy = self.x - 1920 / 2, self.y - 1080 / 2
                print(f"Trigger: Moving mouse from ({x}, {y}) to ({self.x}, {self.y})")
                command = f"{dx},{dy}\n"
                self.ser.write(command.encode())
            else:
                print(f"Trigger: No target detected)")
    
    def on_press(self, key):
        x, y = self.mouse.position
        if key == KeyCode.from_char('`'):
            if self.x != -1 and self.y != -1:
                dx, dy = 0 - x, 0 - y
                # dx, dy = self.x - x, self.y - y
                # dx, dy = self.x - 1920 / 2, self.y - 1080 / 2
                # print(f"Trigger: Moving mouse from ({x}, {y}) to ({self.x}, {self.y})")
                command = f"{dx},{dy}\n"
                self.ser.write(command.encode())
            else:
                print(f"Trigger: No target detected)")
    
    def on_release(self, key):
        if key == Key.ctrl_l:
            print(f"Trigger: Stop moving mouse")
            dx, dy = 30, -30
            command = f"{dx},{dy}\n"
            self.ser.write(command.encode())
        
            
if __name__ == '__main__':
    hand = Hand()
    hand.work()
    while True:
        pass
            
        

