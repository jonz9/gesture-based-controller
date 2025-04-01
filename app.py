import tkinter as tk
import argparse

from gesture_recognition.camera import main as gesture_recognition_main
from tkinter import ttk


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=bool, default=True)
    parser.add_argument("--width", type=int, default=1100)
    parser.add_argument("--height", type=int, default=700)
    parser.add_argument("--max_num_hands", type=int, default=1)
    parser.add_argument("--use_static_image_mode", type=bool, default=True)
    parser.add_argument(
        "--min_detection_confidence",
        help="--min_detection_confidence",
        type=float,
        default=0.7,
    )
    parser.add_argument(
        "--min_tracking_confidence",
        help="--min_tracking_confidence",
        type=int,
        default=0.5,
    )

    args = parser.parse_args()

    return args


# def save_settings():
#     sensitivity = sensitivity_var.get()
#     gesture_click = gesture_click_var.get()
#     gesture_scroll = gesture_scroll_var.get()
#     print(f"Saved Settings: Sensitivity={sensitivity}, Click Gesture={gesture_click}, Scroll Gesture={gesture_scroll}")

# def run():
#     global sensitivity_var, gesture_click_var, gesture_scroll_var

#     # window setup
#     root = tk.Tk()
#     root.title("Gesture Navigation Settings")
#     root.geometry("800x600")

#     #===== Configurations =====
#     """
#     Available Gestures
#     - Thumb Up/Down
#     - Index Up/Down
#     - Middle Up/Down
#     - Ring Up/Down
#     - Pinky Up/Down
#     - Palm
#     - Close Hand

#     Gesture Functionalities
#     - Volumn Up/Down: thumb up/down
#     - Brightness Up/Down: index up/down
#     - Media Control (Play/Pause, Next, Previous):
#     - Mouse Control (Move, Click, Scroll):
#     - Microphone Control (Mute, Unmute):
#     - Screen Capture (Take Screenshot, Record Screen):
#     """

#     # sensitivity control
#     sensitivity_var = tk.DoubleVar(value=1.0)
#     tk.Label(root, text="Mouse Sensitivity").pack()
#     sensitivity_slider = ttk.Scale(root, from_=0.5, to=3.0, variable=sensitivity_var, orient="horizontal")
#     sensitivity_slider.pack()

#     # gesture control
#     tk.Label(root, text="Click Gesture").pack()
#     gesture_click_var = tk.StringVar(value="Pinch Thumb & Index")
#     gesture_click_dropdown = ttk.Combobox(root, textvariable=gesture_click_var, values=["Pinch Thumb & Index", "Tap Palm", "Close Hand"])
#     gesture_click_dropdown.pack()

#     # scroll gesture
#     tk.Label(root, text="Scroll Gesture").pack()
#     gesture_scroll_var = tk.StringVar(value="Swipe Up/Down")
#     gesture_scroll_dropdown = ttk.Combobox(root, textvariable=gesture_scroll_var, values=["Swipe Up/Down", "Rotate Hand", "Tilt Wrist"])
#     gesture_scroll_dropdown.pack()

#     # save
#     save_button = ttk.Button(root, text="Save Settings", command=save_settings)
#     save_button.pack(pady=10)

#     # Start the Tkinter event loop
#     root.mainloop()

# main entry point
if __name__ == "__main__":
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    max_num_hands = args.max_num_hands
    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    use_brect = True

    gesture_recognition_main(
        cap_device,
        cap_width,
        cap_height,
        use_static_image_mode,
        min_detection_confidence,
        min_tracking_confidence,
        use_brect,
    )
