import cv2
import numpy as np
import torch
from ultralytics import YOLO

class BrainYOLO:
    def __init__(self):
        self.model = YOLO('weights_yolo/best.pt').cuda()

    def test(self, img_path):
        img = cv2.imread(img_path)
        results = self.model.predict(img, classes=1)
        return results
    
    def align_target_points(self, target_points):
        for i in range(len(target_points)):
            target_points[i][0] += 720
            target_points[i][1] += 300
        return target_points
    
    def think(self, img):
        results = self.model.predict(img, verbose=False, classes=1)
        processed_img = results[0].plot()
        target_points = []
        for box in results[0].boxes:
            x_center, y_center, width, height = box.xywh.tolist()[0]
            target_points.append([x_center, y_center])
            
            
        # Visualize the results
        cv2.namedWindow('AEye', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('AEye', 960, 540)
        cv2.resizeWindow('AEye', 480, 480)

        cv2.imshow('AEye', processed_img)
        
        return processed_img, self.align_target_points(target_points)
        
        
if __name__ == '__main__':
    brain = BrainYOLO()
    results = brain.test('data/valorant0.jpg')
    print(len(results))
    # for result in results:
    #     print(result)
    centers = []
    for result in results:
        for box in result.boxes:
            x_center, y_center, width, height = box.xywh.tolist()[0]
            centers.append([x_center, y_center])
            print(f"中心坐标：{x_center}, {y_center}，宽高：{width}, {height}， 类别：{brain.model.names[int(box.cls)]}, 置信度：{box.conf.item():.2f}")
    annotated_frame = results[0].plot()
    cv2.imshow('annotated_frame', annotated_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()