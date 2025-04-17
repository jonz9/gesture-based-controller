import csv
import copy
import cv2 as cv
import numpy as np
import mediapipe as mp

from collections import deque
from collections import Counter

from utils import FpsCalc
from landmarks import calc_landmark_list
from landmarks import pre_process_landmark
from landmarks import draw_landmarks
from pointhistory import draw_point_history
from pointhistory import pre_process_point_history
from models import KeyPointClassifier
from models import PointHistoryClassifier
# fix import errors


# main function
def gesture_recognition_main(
    cap_device,
    cap_width,
    cap_height,
    max_num_hands,
    use_static_image_mode,
    min_detection_confidence,
    min_tracking_confidence,
    use_brect,
):
    use_brect = True

    # Camera setup
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # FPS calculation
    FpsCalc = FpsCalc(buffer_len=10)

    # Load mediapipe and classification models for hand detection
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=max_num_hands,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    keypoint_classifier = KeyPointClassifier()
    point_history_classifier = PointHistoryClassifier()

    # Read labels for gesture classification
    with open(
        "model/keypoint_classifier/keypoint_classifier_label.csv", encoding="utf-8-sig"
    ) as f:
        """
        Isolates first column as gesture labels:
        0:
        1:
        2:
        3:
        """

        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]

    with open(
        "model/point_history_classifier/point_history_classifier_label.csv",
        encoding="utf-8-sig",
    ) as f:
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

    def logging_csv(number, mode, landmark_list, point_history_list):
        if mode == 0:
            pass
        if mode == 1 and (0 <= number <= 9):
            csv_path = "model/keypoint_classifier/keypoint.csv"
            with open(csv_path, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *landmark_list])
        if mode == 2 and (0 <= number <= 9):
            csv_path = "model/point_history_classifier/point_history.csv"
            with open(csv_path, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *point_history_list])
        return

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
            landmark_array = np.append(
                landmark_array, [[landmark_x, landmark_y]], axis=0
            )

        x, y, w, h = cv.boundingRect(landmark_array)
        return [x, y, x + w, y + h]

    def draw_bounding_rect(use_brect, image, brect):
        if use_brect:
            cv.rectangle(
                image, (brect[0], brect[1]), (brect[2], brect[3]), (0, 0, 0), 1
            )
        return image

    # drawing gesture info text on screen
    def draw_info_text(image, brect, handedness, hand_sign_text, finger_gesture_text):
        cv.rectangle(
            image, (brect[0], brect[1]), (brect[2], brect[1] - 22), (0, 0, 0), -1
        )

        info_text = handedness.classification[0].label[0:]
        if hand_sign_text != "":
            info_text = info_text + ":" + hand_sign_text
        cv.putText(
            image,
            info_text,
            (brect[0] + 5, brect[1] - 4),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
            cv.LINE_AA,
        )

        if finger_gesture_text != "":
            cv.putText(
                image,
                "Finger Gesture:" + finger_gesture_text,
                (10, 60),
                cv.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 0),
                4,
                cv.LINE_AA,
            )
            cv.putText(
                image,
                "Finger Gesture:" + finger_gesture_text,
                (10, 60),
                cv.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2,
                cv.LINE_AA,
            )

        return image

    # drawing utils info on screen
    def draw_info(image, fps, mode, number):
        cv.putText(
            image,
            "FPS:" + str(fps),
            (10, 30),
            cv.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 0),
            4,
            cv.LINE_AA,
        )
        cv.putText(
            image,
            "FPS:" + str(fps),
            (10, 30),
            cv.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
            cv.LINE_AA,
        )

        mode_string = ["Logging Key Point", "Logging Point History"]
        if 1 <= mode <= 2:
            cv.putText(
                image,
                "MODE:" + mode_string[mode - 1],
                (10, 90),
                cv.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1,
                cv.LINE_AA,
            )
            if 0 <= number <= 9:
                cv.putText(
                    image,
                    "NUM:" + str(number),
                    (10, 110),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    1,
                    cv.LINE_AA,
                )
        return image

    # Main loop
    while True:
        fps = FpsCalc.get()

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
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                pre_processed_point_history_list = pre_process_point_history(
                    point_history
                )

                # write to dataset
                logging_csv(
                    number,
                    mode,
                    pre_processed_landmark_list,
                    pre_processed_point_history_list,
                )

                # hand sign classification
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                if hand_sign_id == 2:
                    point_history.append(landmark_list[8])
                else:
                    point_history.append([0, 0])

                # finger gesture classification
                finger_gesture_id = 0
                point_history_len = len(pre_processed_point_history_list)
                if point_history_len == (history_length * 2):
                    finger_gesture_id = point_history_classifier(
                        pre_processed_point_history_list
                    )

                    # Calculates the gesture IDs in the latest detection
                    finger_gesture_history.append(finger_gesture_id)
                    most_common_fg_id = Counter(finger_gesture_history).most_common()

                    # Drawing part
                    debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                    debug_image = draw_landmarks(debug_image, landmark_list)
                    debug_image = draw_info_text(
                        debug_image,
                        brect,
                        handedness,
                        keypoint_classifier_labels[hand_sign_id],
                        point_history_classifier_labels[most_common_fg_id[0][0]],
                    )
                else:
                    point_history.append([0, 0])

                debug_image = draw_point_history(debug_image, point_history)
                debug_image = draw_info(debug_image, fps, mode, number)

                # screen
                cv.imshow("Hand Gesture Recognition", debug_image)

        cap.release()
        cv.destroyAllWindows()
