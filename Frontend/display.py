from pygame import display, FULLSCREEN, mouse, RESIZABLE as PYRES, cursors, image
from os import path
from Frontend.settings import WIDTH, HEIGHT, RESIZABLE, FULL_SCREEN_VIEW


class Display:
    __LOGO_FILE = "Purps.png"

    def __init__(self):
        self.width, self.height = WIDTH, HEIGHT
        self.window = display.set_mode((self.width, self.height), PYRES if RESIZABLE else None)
        self.check_full_screen()
        self.__set_title()
        self.__set_logo()

    def __set_logo(self):
        logo_image = image.load(path.join("Frontend\Mania_Window\Img", self.__LOGO_FILE)).convert_alpha()
        display.set_icon(logo_image)

    @staticmethod
    def __set_title():
        display.set_caption("Ringo Mania!")

    def check_full_screen(self, full_screen=False):
        if FULL_SCREEN_VIEW or full_screen:
            self.width, self.height = 1600, 900
            self.window = display.set_mode((self.width, self.height), FULLSCREEN)
            mouse.set_visible(False)
            mouse.set_cursor(cursors.arrow)

    @property
    def get_window_size(self):
        return self.width, self.height

    @property
    def center(self) -> tuple[int, int]:
        return self.width // 2, self.height // 2

    @staticmethod
    def center_window_element(width, element_width):
        return width - element_width / 2

    def check_window_size(self) -> bool:
        width, height = self.window.get_size()
        changed_window_size = width != self.width or height != self.height
        if changed_window_size:
            self.width, self.height = width, height
            return True
        else:
            return False
