from collections import deque
import csv
import copy
import cv2 as cv
import numpy as np
import mediapipe as mp

from utils import CvFpsCalc
from models import KeyPointClassifier
from models import PointHistoryClassifier

def main(cap_device, cap_width, cap_height, max_num_hands, use_static_image_mode, min_detection_confidence, min_tracking_confidence, use_brect):
  use_brect = True
  
  # Camera setup
  cap = cv.VideoCapture(cap_device)
  cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
  cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

  # FPS calculation
  cvFpsCalc = CvFpsCalc(buffer_len=10)

  # Load mediapipe and classification models for hand detection
  mp_hands = mp.solutions.hands
  hands = mp_hands.Hands(
    model_complexity=0,
    max_num_hands=max_num_hands,
    min_detection_confidence=min_detection_confidence,
    min_tracking_confidence=min_tracking_confidence,
  )

  keypoint_classifier = KeyPointClassifier()
  point_history_classifier = PointHistoryClassifier()

  # Read labels for gesture classification
  with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
    """
    Isolates first column as gesture labels:
    0: 
    1:
    2:
    3:
    """
    
    keypoint_classifier_labels = csv.reader(f)
    keypoint_classifier_labels = [
      row[0] for row in keypoint_classifier_labels
    ]
  
  with open('model/point_history_classifier/point_history_classifier_label.csv', encoding='utf-8-sig') as f:
    """
    Isolates first column as dynamic gesture labels:
    0: 
    1:
    2:
    """

    point_history_classifier_labels = csv.reader(f)
    point_history_classifier_labels = [
      row[0] for row in point_history_classifier_labels
    ]

  # Coordionate History for point history classification (dynamic gestures)
  history_length = 16
  point_history = deque(maxlen=history_length)
  finger_gesture_history = deque(maxlen=history_length)
  
  # Mode 0: Gesture recognition
  mode = 0
  
  def logging_csv(gesture_id, point_history):
    if point_history is None:
      point_history = []
    csv_path = 'model/point_history_classifier/point_history.csv'
    with open(csv_path, 'a') as f:
      writer = csv.writer(f)
      writer.writerow([gesture_id] + point_history)

  def select_mode(key, mode):
    number = -1
    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48
    if key == 110:  # n
        mode = 0
    if key == 107:  # k
        mode = 1
    if key == 104:  # h
        mode = 2
    return number, mode
  
  # calculates bounding box for hand in camera
  def calc_bounding_rect(image, landmarks):
      image_width, image_height = image.shape[1], image.shape[0]

      landmark_array = np.empty((0, 2), int)

      for _, landmark in enumerate(landmarks.landmark):
          landmark_x = min(int(landmark.x * image_width), image_width - 1)
          landmark_y = min(int(landmark.y * image_height), image_height - 1)

          landmark_array = np.append(landmark_array, [[landmark_x, landmark_y]], axis=0)
          
      x, y, w, h = cv.boundingRect(landmark_array)

      return [x, y, x + w, y + h]
  

  # calculate landmarks and append to landmarks list
  def calc_landmarks(image, landmarks):
     image_width, image_height = image.shape[1], image.shape[0]

     landmark_point = []

     for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point.append((landmark_x, landmark_y))

     return landmark_point
  

  def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
      

  # Main loop
  while True:
    fps = cvFpsCalc.get()

    # ESC: end key
    key = cv.waitKey(10)
    if key == 27: 
      break
    number, mode = select_mode(key, mode)

    # capture frames from camera
    ret, image = cap.read()
    if not ret:
      break
    image = cv.flip(image, 1)
    debug_image = copy.deepcopy(image)

    # detection
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True

    # draw landmarks if detected
    if results.multi_hand_landmarks is not None:
      for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
        brect = calc_bounding_rect(debug_image, hand_landmarks)
        landmark_list = calc_landmark_list(debug_image, hand_landmarks)

        pre_processed_landmark_list = pre_process_landmark(landmark_list)
        pre_processed_point_history_list = pre_process_point_history(point_history)

        # write to dataset
        logging_csv(number, mode, pre_processed_landmark_list, pre_processed_point_history_list)
  
        # hand sign classification
        hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
        if hand_sign_id == 2:
          point_history.append(landmark_list[8])
        else:
          point_history.append([0, 0])


        