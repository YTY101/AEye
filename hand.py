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
        self.switch_listener = KeyboardListener(on_press=self.on_press_switch)
        self.listener = Listener(on_click=self.on_click)
        # self.listener = KeyboardListener(on_press=self.on_press_fps)
        self.mouse = Controller()
        self.port = 'COM8'
        self.baudrate = 115200
        self.ser = serial.Serial(self.port, self.baudrate)
        self.pid = PIDController(0.5, 0, 0)
        self.executing = False
        self.switch = False
        
    def work(self):
        self.switch_listener.start()
        self.listener.start()

    def get_mouse_position(self):
        x, y = self.mouse.position
        return x, y
    
    def send_command(self, dx, dy):
        command = f"{dx},{dy}\n"
        self.ser.write(command.encode())
    
    def split_movement(self, dx, dy):
        step = 10
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
        if button == Button.middle and pressed and not self.executing:
            self.executing = True
            current_x, current_y = self.get_mouse_position()
            target_x, target_y = (self.x, self.y)
            if (self.x != -1 and self.y != -1):
                dx, dy = target_x - current_x, target_y - current_y
                for step_dx, step_dy in self.split_movement(dx, dy):
                    self.send_command(step_dx, step_dy)
                    time.sleep(0.001)  # 给 MCU
                self.send_command("x", "x")
                print(f"Trigger: Moving mouse from ({current_x}, {current_y}) to ({target_x}, {target_y})")
                
            else:
                self.send_command("x", "x")
                print(f"Trigger: No target detected")
            self.executing = False
    
    
    def on_click_pid(self, x, y, button, pressed):
        if button == Button.middle and pressed:
            target_x, target_y = (self.x, self.y)
            if (self.x != -1 and self.y != -1):
                current_x, current_y = self.get_mouse_position()
                print(f"Trigger: Moving mouse from ({current_x}, {current_y}) to ({target_x}, {target_y})")
                
                while(abs(target_x - current_x) > 10 or abs(target_y - current_y) > 10):
                    target_x, target_y = (self.x, self.y)
                    dx, dy = self.pid.compute((current_x, current_y), (target_x, target_y))
                    self.send_command(dx, dy)
                    current_x, current_y = self.get_mouse_position()
                    # print(f"PID Track: {current_x}, {current_y}")
                    time.sleep(0.01)  # 给 MCU
            else:
                print(f"Trigger: No target detected")
    
    def on_click_test(self, x, y, button, pressed):
        if button == Button.left and pressed:
            print("CLICKED")
            
    def on_click_fps(self, x, y, button, pressed):
        if self.switch and button == Button.middle and not pressed and not self.executing:
            self.executing = True
            current_x, current_y = 1920 / 2, 1080 / 2
            if (self.x != -1 and self.y != -1):
                target_x, target_y = (self.x, self.y)
                dx, dy = target_x - current_x, target_y - current_y
                for step_dx, step_dy in self.split_movement(dx, dy):
                    self.send_command(step_dx, step_dy)
                    time.sleep(0.01)  # 给 MCU
                self.send_command("x", "x")
                print(f"Trigger: Moving mouse from ({current_x}, {current_y}) to ({target_x}, {target_y})")
                
            else:
                self.send_command("x", "x")
                print(f"Trigger: No target detected")
            self.executing = False

    def on_press(self, key):
        if key == KeyCode.from_char('f'):
            current_x, current_y = self.get_mouse_position()
            if (self.x != -1 and self.y != -1):
                target_x, target_y = (self.x, self.y)
                print(f"Trigger: Moving mouse from ({current_x}, {current_y}) to ({target_x}, {target_y})")
                dx, dy = target_x - current_x, target_y - current_y
                for step_dx, step_dy in self.split_movement(dx, dy):
                    self.send_command(step_dx, step_dy)
                    time.sleep(0.0001)  # 给 MCU
                self.send_command("x", "x")
            else:
                print(f"Trigger: No target detected")
                
    
    def on_press_pid(self, key):
        # x, y = self.get_mouse_position()
        if key == KeyCode.from_char('f'):
            target_x, target_y = (self.x, self.y)
            if (self.x != -1 and self.y != -1):
                current_x, current_y = self.get_mouse_position()
                print(f"Trigger: Moving mouse from ({current_x}, {current_y}) to ({target_x}, {target_y})")
                
                while(abs(target_x - current_x) > 10 or abs(target_y - current_y) > 10):
                    target_x, target_y = (self.x, self.y)
                    dx, dy = self.pid.compute((current_x, current_y), (target_x, target_y))
                    self.send_command(dx, dy)
                    current_x, current_y = self.get_mouse_position()
                    print(f"PID Track: {current_x}, {current_y}")
                    time.sleep(0.01)  # 给 MCU
            else:
                print(f"Trigger: No target detected")

    def on_press_fps(self, key):
        if key == KeyCode.from_char('f'):
            current_x, current_y = 1920 / 2, 1080 / 2
            if (self.x != -1 and self.y != -1):
                target_x, target_y = (self.x, self.y)
                print(f"Trigger: Moving mouse from ({current_x}, {current_y}) to ({target_x}, {target_y})")
                dx, dy = target_x - current_x, target_y - current_y
                for step_dx, step_dy in self.split_movement(dx, dy):
                    self.send_command(step_dx, step_dy)
                    time.sleep(0.0007)  # 给 MCU
                self.send_command("x", "x")
                
            else:
                print(f"Trigger: No target detected")
                
                
            # current_x, current_y = 1920 / 2, 1080 / 2
            # if (self.x != -1 and self.y != -1):
            #     target_x, target_y = (self.x, self.y)
            #     print(f"Trigger: Moving mouse from ({current_x}, {current_y}) to ({target_x}, {target_y})")
            #     dx, dy = target_x - current_x, target_y - current_y
            #     for step_dx, step_dy in self.split_movement(dx, dy):
            #         self.send_command(step_dx, step_dy)
            #         time.sleep(0.001)  # 给 MCU
            # else:
            #     print(f"Trigger: No target detected")
                
                
    def on_press_pid_fps(self, key):
        if key == KeyCode.from_char('f'):
            target_x, target_y = 1920 / 2, 1080 / 2
            if (self.x != -1 and self.y != -1):
                current_x, current_y = (self.x, self.y)
                print(f"Trigger: Moving mouse from ({current_x}, {current_y}) to ({target_x}, {target_y})")
                
                repeat = 0
                last_x, last_y = -1, -1
                while(abs(target_x - current_x) > 5 or abs(target_y - current_y) > 5):
                    dx, dy = self.pid.compute((current_x, current_y), (target_x, target_y))
                    self.send_command(-dx, -dy)
                    current_x, current_y = (self.x, self.y)
                    print(f"PID Track: {current_x}, {current_y} repeat: {repeat}")
                    if current_x == last_x and current_y == last_y:
                        repeat += 1
                        if repeat > 10:
                            print(f"Trigger: Target lost")
                            break
                    else:
                        last_x, last_y = current_x, current_y
                        repeat = 0
                    if current_x == -1 or current_y == -1:
                        print(f"Trigger: Target lost")
                        break
                    time.sleep(0.01)  # 给 MCU
            else:
                print(f"Trigger: No target detected")

    def on_press_switch(self, key):
        if key == KeyCode.from_char('`'):
            if self.switch:
                print("Turn Off")
            else:
                print("Turn On")
            self.switch = not self.switch        

    def on_release(self, key):
        if key == Key.ctrl_l:
            print(f"Trigger: Stop moving mouse")
            dx, dy = 30, -30
            command = f"{dx},{dy}\n"
            self.ser.write(command.encode())
        
            
if __name__ == '__main__':
    hand = Hand()
    hand.set_target(1920 / 2, 1080 / 2)
    hand.work()
    
    while True:
        pass
            
        

