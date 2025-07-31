import cv2

def list_available_cameras(max_index=10):
    print("Searching for available camera indices...")
    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            print(f"Camera index {index} is available.")
            cap.release()
        else:
            print(f"Camera index {index} is NOT available.")

list_available_cameras()
