import pyautogui

class Control:
    def __init__(self):
        pass

    def two_finger_scroll(self, direction: str):
        if direction == "up":
            pyautogui.scroll(120)
        elif direction == "down":
            pyautogui.scroll(-120)

    def volumn_up(self):
        pyautogui.press('volumeup')

    def volumn_down(self):
        pyautogui.press('volumedown')

    def volumn_mute_unmute(self):
        pyautogui.press('volumemute')

    def video_pause_play(self):
        pyautogui.press('playpause')

    def skip_forward(self):
        pyautogui.press('nexttrack')

    def skip_backward(self):
        pyautogui.press('prevtrack')

    def power(self):
        pass
    
    def notification_sidebar(self):
        pyautogui.hotkey('win', 'a')

