from eye import Eye
from hand import Hand
from brain import Brain
import pygetwindow as gw
import threading
import queue
import cv2

class Body:
    def __init__(self, window_title):
        self.window_title = window_title
        self.eye = Eye(window_title)
        self.hand = Hand()
        self.brain = Brain(cpu=False)
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.original_out = cv2.VideoWriter("records/recorded_original.mp4", self.fourcc, 20.0, (720, 405))
        self.processed_out = cv2.VideoWriter("records/recorded_processed.mp4", self.fourcc, 20.0, (720, 405))
        
        
    def run(self):
        self.hand.work()
        for i, frame in enumerate(self.eye.start_looking()):
            processed_frame = self.brain.think(frame)
            print(f"Frame {i} processed {frame.shape}")
            self.original_out.write(frame)
            self.processed_out.write(processed_frame)
            