from Foundation import NSObject
from objc import super

class Control(NSObject):
    def __init__(self):
        super(Control, self).__init__()

    def two_finger_scroll(self, direction: str):
        if direction == "up":
            self.scroll_wheel(0, 1)
        elif direction == "down":
            self.scroll_wheel(0, -1)

    def volumn_up(self):
        self.key_down(0x6F)
        self.key_up(0x6F)

    def volumn_down(self):
        self.key_down(0x67)
        self.key_up(0x67)

    def volumn_mute_unmute(self):
        self.key_down(0x6D)
        self.key_up(0x6D)

    def video_pause_play(self):
        self.key_down(0x64)
        self.key_up(0x64)

    def skip_forward(self):
        self.key_down(0x65)
        self.key_up(0x65)

    def skip_backward(self):
        self.key_down(0x62)
        self.key_up(0x62)

    def power(self):
        self.key_down(0x7F)
        self.key_up(0x7F)
    
    def notification_sidebar(self):
        self.key_down(0x61)
        self.key_up(0x61)

    def brightness_up(self):
        self.key_down(0x78)
        self.key_up(0x78)

    def brightness_down(self):
        self.key_down(0x7A)
        self.key_up(0x7A)