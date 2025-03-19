import tkinter as tk
from tkinter import ttk

def save_settings():
    sensitivity = sensitivity_var.get()
    gesture_click = gesture_click_var.get()
    gesture_scroll = gesture_scroll_var.get()
    print(f"Saved Settings: Sensitivity={sensitivity}, Click Gesture={gesture_click}, Scroll Gesture={gesture_scroll}")

def run():
    global sensitivity_var, gesture_click_var, gesture_scroll_var

    # window setup
    root = tk.Tk()
    root.title("Gesture Navigation Settings")
    root.geometry("500x300")

    # sensitivity control
    sensitivity_var = tk.DoubleVar(value=1.0)
    tk.Label(root, text="Mouse Sensitivity").pack()
    sensitivity_slider = ttk.Scale(root, from_=0.5, to=3.0, variable=sensitivity_var, orient="horizontal")
    sensitivity_slider.pack()

    # gesture control
    tk.Label(root, text="Click Gesture").pack()
    gesture_click_var = tk.StringVar(value="Pinch Thumb & Index")
    gesture_click_dropdown = ttk.Combobox(root, textvariable=gesture_click_var, values=["Pinch Thumb & Index", "Tap Palm", "Close Hand"])
    gesture_click_dropdown.pack()

    tk.Label(root, text="Scroll Gesture").pack()
    gesture_scroll_var = tk.StringVar(value="Swipe Up/Down")
    gesture_scroll_dropdown = ttk.Combobox(root, textvariable=gesture_scroll_var, values=["Swipe Up/Down", "Rotate Hand", "Tilt Wrist"])
    gesture_scroll_dropdown.pack()

    # save
    save_button = ttk.Button(root, text="Save Settings", command=save_settings)
    save_button.pack(pady=10)

# main entry point
if __name__ == "__main__":
  run()