from eye import Eye
from hand import Hand
from brain import Brain
from body import Body
import pygetwindow as gw
WINDOW_TITLE = "Untitled"

def main():
    windows_name = []
    for idx, window in enumerate(gw.getAllTitles()):
        if window.strip():
            print(idx, ": ", window)
            windows_name.append(window)

    
    index = input("Input the window index: ")
    WINDOW_TITLE = windows_name[int(index)]
    body = Body(WINDOW_TITLE)
    body.run()
    
if __name__ == '__main__':
    main()