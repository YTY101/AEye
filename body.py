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
        target_points = []
        for i, frame in enumerate(self.eye.start_looking()):
            processed_frame, target_points = self.brain.think(frame, track=1, smooth=1)
            # print(f"Frame {i} processed {frame.shape}")
            # print("target points: ", target_points)
            if len(target_points) > 0:
                self.hand.set_target(target_points[0][0], target_points[0][1])
            else:
                self.hand.set_target(-1, -1)
            self.original_out.write(frame)
            self.processed_out.write(processed_frame)
            