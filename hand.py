import time
import pyautogui
from pynput.mouse import Button, Listener, Controller
from pynput.keyboard import Key, KeyCode, Listener as KeyboardListener
import ctypes
import pydirectinput
import serial

class PIDController:
    def __init__(self, kp, ki, kd, max_output=127, min_output=-127):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_output = max_output
        self.min_output = min_output
        self.integral_x = 0
        self.integral_y = 0
        self.prev_error_x = 0
        self.prev_error_y = 0

    def compute(self, current, target):
        error_x = target[0] - current[0]
        error_y = target[1] - current[1]

        self.integral_x += error_x
        self.integral_y += error_y

        derivative_x = error_x - self.prev_error_x
        derivative_y = error_y - self.prev_error_y

        output_x = self.kp * error_x + self.ki * self.integral_x + self.kd * derivative_x
        output_y = self.kp * error_y + self.ki * self.integral_y + self.kd * derivative_y

        self.prev_error_x = error_x
        self.prev_error_y = error_y

        # 限制输出在 [-127, 127]
        output_x = max(self.min_output, min(self.max_output, int(round(output_x))))
        output_y = max(self.min_output, min(self.max_output, int(round(output_y))))

        return output_x, output_y


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
        self.pid = PIDController(0.3, 0, 0)
    
    def work(self):
        self.listener.start()

    def get_mouse_position(self):
        x, y = self.mouse.position
        return x, y
    
    def send_command(self, dx, dy):
        command = f"{dx},{dy}\n"
        self.ser.write(command.encode())
    
    def split_movement(self, dx, dy):
        step = 64
        """将超过 ±127 的移动分成多个小步"""
        steps = []
        while dx != 0 or dy != 0:
            step_dx = max(-step, min(step, dx))
            step_dy = max(-step, min(step, dy))
            steps.append((step_dx, step_dy))
            dx -= step_dx
            dy -= step_dy
        return steps

    
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
                print(f"Trigger: No target detected")
    
    def on_press(self, key):
        # x, y = self.get_mouse_position()
        if key == KeyCode.from_char('`'):
            # self.set_target(956, 442)
            target_x, target_y = (self.x, self.y)
            if (self.x != -1 and self.y != -1):
                current_x, current_y = self.get_mouse_position()
                print(f"Trigger: Moving mouse from ({current_x}, {current_y}) to ({target_x}, {target_y})")
                
                while(abs(target_x - current_x) > 10 or abs(target_y - current_y) > 10):
                    dx, dy = self.pid.compute((current_x, current_y), (target_x, target_y))
                    self.send_command(dx, dy)
                    current_x, current_y = self.get_mouse_position()
                    print(f"PID Track: {current_x}, {current_y}")
                    time.sleep(0.01)  # 给 MCU
            else:
                print(f"Trigger: No target detected")

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
            
        

