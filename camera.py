import cv2

def open_camera():
    return cv2.VideoCapture(0)

def get_frame(cap):
    ret, frame = cap.read()
    return frame if ret else None

def close_camera(cap):
    if cap:
        cap.release()