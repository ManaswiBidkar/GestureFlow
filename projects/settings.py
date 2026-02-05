DISC_GESTURE = [True, True, False, False, True]

RIGHT_DISC_ANGLE = 'rightAngle'
RIGHT_POINTER_COORDS = 'rightPointer'
RIGHT_ACTION_COORDS = 'rightAction'


LEFT_DISC_ANGLE = 'leftAngle'
LEFT_POINTER_COORDS = 'leftPointer'
LEFT_ACTION_COORDS = 'leftAction'

RESET_STATES = [
    RIGHT_DISC_ANGLE, RIGHT_POINTER_COORDS, RIGHT_ACTION_COORDS,
    LEFT_DISC_ANGLE, LEFT_POINTER_COORDS, LEFT_ACTION_COORDS,
]

SLIDE_NUMBER = 'slideNumber'
CURRENT_TOOL = 'currentTool'


DEFAULT_STATE_DICT = {

    RIGHT_DISC_ANGLE: None,
    RIGHT_POINTER_COORDS: None,
    RIGHT_ACTION_COORDS: None,

    LEFT_DISC_ANGLE: None,
    LEFT_POINTER_COORDS: None,
    LEFT_ACTION_COORDS: None,

    SLIDE_NUMBER: 0,
}

ANGLE_UNIT = 20
IMAGE_PATH = 'presentations'


POINTING_GESTURE = 'pointingGesture'
ANNOTATING_GESTURE = 'annotatingGesture'
ERASE_GESTURE = 'eraseGesture'
SLIDE_CHANGE_GESTURE = 'slideChangeGesture'
POINTER_SIZE_CHANGE_GESTURE = 'pointerSizeChangeGesture'


GESTURES = {
    POINTING_GESTURE: ([False, True, False, False, False]),
    ANNOTATING_GESTURE: ([False, True, True, False, False]),
    ERASE_GESTURE: ([True, True, True, True, True]),
    SLIDE_CHANGE_GESTURE: ([True, True, True, True, True], [False, True, True, True, False]),
    POINTER_SIZE_CHANGE_GESTURE: ([False, True, True, True, True], [False, True, True, True, False]),
}

GESTURE_FILE = 'gestures.json'
