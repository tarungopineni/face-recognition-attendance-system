import tkinter as tk
from PIL import Image, ImageTk
import cv2
from attendance_engine import mark_attendance
from face_engine import verify_face

FACE_DB_PATH = r"C:\Users\tarun\OneDrive\Documents\face_attendance\faces"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Attendance")
        self.root.geometry("800x600")

        tk.Label(root, text="Face Attendance System", font=("Segoe UI", 20, "bold")).pack(pady=15)

        self.roll = tk.Entry(root, font=("Segoe UI", 14), bd=3)
        self.roll.pack(pady=10)

        self.status = tk.Label(root, font=("Segoe UI", 12))
        self.status.pack(pady=10)

        self.video = tk.Label(root)
        self.video.pack(pady=10)

        self.btn = tk.Button(root, text="Verify", font=("Segoe UI", 12), bd=3, command=self.start)
        self.btn.pack(pady=10)

        self.cap = None
        self.running = False
        self.show_icon()

    def show_icon(self):
        img = Image.open("camera_icon.png").resize((400,300))
        self.icon = ImageTk.PhotoImage(img)
        self.video.config(image=self.icon)

    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.update()
        self.root.after(1500, self.capture)

    def update(self):
        if not self.running: return
        ret, frame = self.cap.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(Image.fromarray(img))
            self.video.imgtk = imgtk
            self.video.config(image=imgtk)
        self.root.after(10, self.update)

    def capture(self):
        self.running = False
        ret, frame = self.cap.read()
        self.cap.release()

        roll = self.roll.get()
        result = verify_face(frame, roll, FACE_DB_PATH)

        if result == "MATCH":
            outcome = mark_attendance(roll)
            if outcome == "CREATED":
                self.status.config(text="🟢 Login Marked", fg="green")
            elif outcome == "UPDATED":
                self.status.config(text="🔵 Logout Marked", fg="blue")
            else:
                self.status.config(text="⚠ Already Completed", fg="orange")
        elif result == "NO_IMAGE":
            self.status.config(text="❌ No image found", fg="red")
        else:
            self.status.config(text="❌ Face not matched", fg="red")

        self.show_icon()

root = tk.Tk()
App(root)
root.mainloop()