import serial
import time

port = 'COM8'  # 根据实际情况修改
baudrate = 115200

ser = serial.Serial(port, baudrate)
# time.sleep(2)  # 等待ESP32启动完成

# 示例：向右移动30像素，向上移动10像素
dx, dy = 30, -30
command = f"{dx},{dy}\n"
ser.write(command.encode())

ser.close()
