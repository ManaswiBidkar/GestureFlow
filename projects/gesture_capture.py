import cv2
from tkinter import ttk
from tkinter import Button, Label, Tk
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
import mediapipe as mp
from gestureflow.tracker import HandTracker
from gestureflow.sample_gesture_trackers import GestureTracker
from gestureflow.definitions import FINGERS_UP, HAND_LABEL
import json
from settings import *
import os


if not os.path.exists(GESTURE_FILE):
    with open(GESTURE_FILE, "w") as gesture_file:
        json.dump(GESTURES, gesture_file)

class FingerTracker(GestureTracker):
    def __init__(self) -> None:
        super().__init__()
        self.fingersUp = []


    def updateState(self, handState):
        self.fingersUp = handState[FINGERS_UP]
    def resetState(self):
        self.fingersUp = []

    def getState(self):
        return self.fingersUp
    
    def track(self, handStates):
        self.gestureFound = False
        for handState in handStates:
            if ((self.trackRightHand and handState[HAND_LABEL] == 'Right')) or ((self.trackLeftHand and handState[HAND_LABEL]== 'Left')):
                self.gestureFound = True
                self.updateState(handState)

        if not self.gestureFound:
            self.resetState()

        for stateTracker in self.stateTrackers:
            stateTracker.update(self.getState())





class WebcamApp:
    def __init__(self, window, window_title, video_source=0, gesture_name='DEFAULT', capture_left=True, capture_right=True):
        self.window = window
        self.window.title(window_title)

        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)

        self.style = ttk.Style()
        self.style.theme_use("clam")  # You can change the theme to your preference

        self.capture_left = capture_left
        self.capture_right = capture_right

        self.label = Label(window, text="Webcam App", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.canvas = ttk.Label(window)
        self.canvas.pack()

        self.btn_capture = ttk.Button(window, text="Capture", command=self.capture)
        self.btn_capture.pack(pady=10)

        self.tracker = HandTracker()
        self.gesture = ()

        self.gesture_name = gesture_name

        if self.capture_left:
            self.left_tracker = FingerTracker()
            self.left_tracker.setTrackRightHand(False)
            self.tracker.add_gesture(self.left_tracker)

        if self.capture_right:
            self.right_tracker = FingerTracker()
            self.right_tracker.setTrackLefttHand(False)
            self.tracker.add_gesture(self.right_tracker)

        with open(GESTURE_FILE) as gesture_file:
            self.gestures = json.load(gesture_file)


        self.update()

    def mainloop(self):
        self.window.mainloop()

    def capture(self):
        from setting_gui import open_setting
        self.vid.release()
        self.window.destroy()
        self.gestures[self.gesture_name] = self.gesture
        with open(GESTURE_FILE, 'w') as gesture_file:
            json.dump(self.gestures, gesture_file)
        open_setting()

    def update(self):
        ret, frame = self.vid.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.tracker.run(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


        if self.capture_left and self.left_tracker.gestureFound:
            self.gesture = self.left_tracker.getState()
        else:
            self.gesture = self.right_tracker.getState()


        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.configure(image=self.photo)
            self.canvas.image = self.photo
        self.window.after(10, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def capture_gesture(gesture_name, capture_left=True, capture_right=True):
    root = ThemedTk(theme="radiance")  # You can change the theme to your preference
    app = WebcamApp(root, window_title=gesture_name, gesture_name=gesture_name, capture_left=capture_left, capture_right=capture_right)
    app.mainloop()

if __name__ == '__main__':
    capture_gesture("Pointer")
