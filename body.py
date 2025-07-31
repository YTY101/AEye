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
        self.brain = Brain(cpu=False)
        self.buffer = []
        
    def run(self):
        self.hand.work()
        for i, frame in enumerate(self.eye.start_looking()):
            if i % 1 == 0:
                self.brain.think(frame)