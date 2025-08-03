import cv2
import numpy as np
import mss
import time
import pygetwindow as gw


class Eye:
    def __init__(self, window_title):

        self.window_title = window_title
        if (window_title == "auto"): 
            # 设置全屏
            self.left = 0
            self.top = 0
            self.width = 1920
            self.height = 1080
            
            # # 480x640
            # self.left = 0
            # self.top = 0
            # self.width = 480
            # self.height = 640
            
            # # 720x405
            # self.left = 600
            # self.top = 338
            # self.width = 720
            # self.height = 405
            
            # # 960x540
            # self.left = 480
            # self.top = 270
            # self.width = 960
            # self.height = 540
            
            # # 1024x1024
            # self.left =448
            # self.top = 28
            # self.width = 1024
            # self.height = 1024
            print(f"Recoding: Fullscreen AREA: ({self.left}, {self.top}, {self.width}, {self.height})")
        else:
            self.window = gw.getWindowsWithTitle(self.window_title)
            if not self.window:
                raise Exception(f"未找到名为 '{self.window_title}' 的窗口")
            self.win = self.window[0]
            self.left, self.top = self.win.left, self.win.top
            self.width, self.height = self.win.width, self.win.height
            print(f"Recoding: {self.window_title} AREA: ({self.left}, {self.top}, {self.width}, {self.height})")


    def start_looking(self):
        # # 设置录屏区域
        self.monitor = {"top": self.top, "left": self.left, "width": self.width, "height": self.height}

        print("start_looking")
        with mss.mss() as sct:
            print("开始录屏，按 Ctrl+C 停止...")
            try:
                while True:
                    frame = np.array(sct.grab(self.monitor))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    # self.out.write(frame)

                    # 显示预览（可选）
                    cv2.namedWindow("Screen", cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("Screen", 960, 540)

                    cv2.imshow("Screen", frame)
                    if cv2.waitKey(1) == 27:  # ESC 键退出预览
                        break
                    
                    frame = cv2.resize(frame, (720, 405))
                    yield frame

            except KeyboardInterrupt:
                print("录制结束。")

