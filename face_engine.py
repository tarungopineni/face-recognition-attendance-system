import cv2
from deepface import DeepFace
import os

def verify_face(live_frame, roll, face_db_path):
    temp_path = "temp.jpeg"
    cv2.imwrite(temp_path, live_frame)

    img_path = os.path.join(face_db_path, f"{roll}.jpeg")
    if not os.path.exists(img_path):
        os.remove(temp_path)
        return "NO_IMAGE"

    try:
        result = DeepFace.verify(img_path, temp_path)
        os.remove(temp_path)
        return "MATCH" if result["verified"] else "NO_MATCH"
    except:
        os.remove(temp_path)
        return "ERROR"