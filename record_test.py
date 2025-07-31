import cv2
import numpy as np
import mss
import time
import pygetwindow as gw


for window in gw.getAllTitles():
    if window.strip():
        print(window)

WINDOW_TITLE = input("Input the window title: ")

window = gw.getWindowsWithTitle(WINDOW_TITLE)
if not window:
    raise Exception(f"未找到名为 '{WINDOW_TITLE}' 的窗口")

win = window[0]
left, top = win.left, win.top
width, height = win.width, win.height
print(f"Recoding: {WINDOW_TITLE} AREA: ({left}, {top}, {width}, {height})")

# 设置录屏区域
monitor = {"top": top, "left": left, "width": width, "height": height}


# 初始化视频编码器
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("recorded.mp4", fourcc, 20.0, (monitor["width"], monitor["height"]))

with mss.mss() as sct:
    print("开始录屏，按 Ctrl+C 停止...")
    try:
        while True:
            frame = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            out.write(frame)

            # 显示预览（可选）
            cv2.imshow("Screen", frame)
            if cv2.waitKey(1) == 27:  # ESC 键退出预览
                break
    except KeyboardInterrupt:
        print("录制结束。")

out.release()
cv2.destroyAllWindows()
