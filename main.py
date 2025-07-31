from eye import Eye
from hand import Hand
from brain import Brain
from body import Body
import pygetwindow as gw
WINDOW_TITLE = "Untitled"

def main():
    windows_name = []
    index = 0
    windows_name.append("auto")
    index += 1
    for window in gw.getAllTitles():
        if window.strip():
            print(index, ": ", window)
            windows_name.append(window)
            index += 1
    
    index = input("Input the window index: ")
    WINDOW_TITLE = windows_name[int(index)]
    body = Body(WINDOW_TITLE)
    body.run()
    
if __name__ == '__main__':
    main()