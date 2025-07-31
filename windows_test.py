import pygetwindow as gw

for window in gw.getAllTitles():
    if window.strip():
        print(window)
