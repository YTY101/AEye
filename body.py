from eye import Eye
from hand import Hand
from brain import Brain
import pygetwindow as gw
import threading
import queue

class Body:
    def __init__(self, window_title):
        self.window_title = window_title
        self.eye = Eye(window_title)
        self.hand = Hand()
        self.brain = Brain()
        self.buffer = []
        
    def run(self):
        self.hand.work()
        for frame in self.eye.start_looking():
            self.brain.think(frame, cpu=False)
            