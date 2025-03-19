Notes Area Ig for now:

csv & collections - used for gesture history for dynamic gestures

itertools & argparse - handles command-line arguments

FPS calculation done by utils - buffer length 10 for FPS smoothing

parser used to set camera parameters

> allows to run something like this:
> python script.py --device 1 --width 1280 --height 720

Uses MediaPipe's hand detection model:

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
static_image_mode=use_static_image_mode,
max_num_hands=1,
min_detection_confidence=min_detection_confidence,
min_tracking_confidence=min_tracking_confidence,
)

- detection confidence is probability threshold for hand detection
- tracking confidence is tracking accuracy for gestures

Keypoint Classifier - model for recognizing static hand gestures
Point History Classifier - model for tracking model-based gestures

we store past movements using history_length variable of 16

- this ensures smooth gesture recognition
