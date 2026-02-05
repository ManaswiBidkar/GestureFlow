from display import DisplayManager
from threading import Thread
from settings import *
from gestureflow.tracker import HandTracker
from gestureflow.sample_gesture_trackers import GestureTracker2D
from gestureflow.sample_state_trackers import RotationCounter, PositionTracker
from gestureflow.sample_runners import Runner
from gestureflow.definitions import *
from state_trackers import *
from gesture_trackers import TwoHandTracker
from settings import GESTURES, POINTING_GESTURE, ANNOTATING_GESTURE, ERASE_GESTURE, SLIDE_CHANGE_GESTURE, POINTER_SIZE_CHANGE_GESTURE
import json
import os
import mediapipe as mp

def prep_gestures():
    global GESTURES
    if os.path.exists(GESTURE_FILE):
        with open(GESTURE_FILE, 'r') as gesture_file:
            GESTURES = json.load(gesture_file)

    global POINTER_GESTURE, ANNOTATION_GESTURE, ERASER_GESTURE, SLIDE_CHANGE_GESTURE_LEFT_HAND, SLIDE_CHANGE_GESTURE_RIGHT_HAND, POINTER_SIZE_CHANGE_GESTURE_LEFT_HAND, POINTER_SIZE_CHANGE_GESTURE_RIGHT_HAND


    POINTER_GESTURE = GESTURES[POINTING_GESTURE]
    ANNOTATION_GESTURE = GESTURES[ANNOTATING_GESTURE]
    ERASER_GESTURE = GESTURES[ERASE_GESTURE]

    SLIDE_CHANGE_GESTURE_LEFT_HAND, SLIDE_CHANGE_GESTURE_RIGHT_HAND = GESTURES[SLIDE_CHANGE_GESTURE]
    POINTER_SIZE_CHANGE_GESTURE_LEFT_HAND, POINTER_SIZE_CHANGE_GESTURE_RIGHT_HAND = GESTURES[POINTER_SIZE_CHANGE_GESTURE]


def present(presentation_path, is_folder=True):
    prep_gestures()
    handTracker = HandTracker()
    handTracker.mp_hands = mp.solutions.hands.Hands(static_image_mode=False, min_detection_confidence=.7, min_tracking_confidence=0.7, max_num_hands=2)

    gesture1 = GestureTracker2D()
    gesture2 = GestureTracker2D()
    gesture3 = GestureTracker2D()
    gesture4 = GestureTracker2D()

    gesture1.setTrackLefttHand(False)
    gesture2.setTrackLefttHand(False)
    gesture3.setTrackLefttHand(False)
    gesture4.setTrackLefttHand(False)

    two_hand_gesture1 = TwoHandTracker()
    two_hand_gesture2 = TwoHandTracker()
    two_hand_gesture3 = TwoHandTracker()

    displayManager = DisplayManager()

    slideNumber = RotationCounter()
    pointer = PositionTracker()

    annotation = AnnotationTracker(displayManager)
    eraser = EraserTracker(displayManager)
    slide_tracker = SlideChangeTracker(displayManager)
    pointer_size_tracker = SizeChangeTracker(displayManager)
    eraser_size_tracker = EraserSizeChangeTracker(displayManager)
    eraser_rotation_size_tracker = RotationCounter()

    eraser_rotation_size_tracker.setMin(1)
    eraser_rotation_size_tracker.setMax(500)

    eraser_rotation_size_tracker.currentValue = 10

    runner = Runner()

    slideNumber.setMin(0)
    slideNumber.setMax(10)
    slideNumber.setDiscUnit(30)

    def set_slide_number(slideNo):
        slideNo = int(slideNo)
        displayManager.setSlideNumber(slideNo)

    def show_pointer(coords):
        displayManager.show_pointer(coords[1])

    def set_eraser_size(size):
        size = int(size)
        displayManager.set_eraser_size(size)


    # gesture1.addGesture(SLIDE_CHANGE_GESTURE)
    gesture2.addGesture(POINTER_GESTURE)
    gesture3.addGesture(ANNOTATION_GESTURE)
    gesture4.addGesture(ERASER_GESTURE)

    two_hand_gesture1.set_left_gesture(SLIDE_CHANGE_GESTURE_LEFT_HAND)
    two_hand_gesture1.set_right_gesture(SLIDE_CHANGE_GESTURE_RIGHT_HAND)

    two_hand_gesture2.set_left_gesture(POINTER_SIZE_CHANGE_GESTURE_LEFT_HAND)
    two_hand_gesture2.set_right_gesture(POINTER_SIZE_CHANGE_GESTURE_RIGHT_HAND)

    gesture1.addStateTracker(slideNumber)
    gesture2.addStateTracker(pointer)
    gesture3.addStateTracker(annotation)
    gesture4.addStateTracker(eraser)
    gesture4.addStateTracker(eraser_rotation_size_tracker)

    two_hand_gesture1.addStateTracker(slide_tracker)
    two_hand_gesture2.addStateTracker(pointer_size_tracker)
    two_hand_gesture3.addStateTracker(eraser_size_tracker)

    handTracker.add_gesture(gesture1)
    handTracker.add_gesture(gesture2)
    handTracker.add_gesture(gesture3)
    handTracker.add_gesture(gesture4)

    handTracker.add_gesture(two_hand_gesture1)
    handTracker.add_gesture(two_hand_gesture2)
    #handTracker.add_gesture(two_hand_gesture3)

    slideNumber.setOnUpdate(set_slide_number)
    pointer.setOnUpdate(show_pointer)
    eraser_rotation_size_tracker.setOnUpdate(set_eraser_size)

    # displayManager.load_from_pptx('test2.pptx')
    if is_folder:
        displayManager.load_folder(presentation_path)
    else:
        displayManager.load_from_pptx(presentation_path)

    trackerThread = Thread(target=runner.loop, args=[handTracker])

    trackerThread.start()

    displayManager.runLoop()

    runner.cap.release()



if __name__ == "__main__":
    present('test')
