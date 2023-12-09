from pygame import display, FULLSCREEN, mouse, RESIZABLE as PYRES, cursors
from Stuff.Ringo_Mania.Frontend.Mania_Window.settings import WIDTH, HEIGHT, RESIZABLE, RECTANGLE_X, RECTANGLE_WIDTH, \
    RECTANGLE_WIDTH_CAP, FULL_SCREEN_VIEW


class Display:
    def __init__(self):
        self.width, self.height = WIDTH, HEIGHT
        self.__rectangle_width = RECTANGLE_WIDTH
        self.__rectangle_x = RECTANGLE_X
        self.window = display.set_mode((self.width, self.height), PYRES if RESIZABLE else None)
        self.check_full_screen()
        self.set_title()

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
    def rectangle_width(self):
        self.__rectangle_width = self.width / 2.2
        if self.__rectangle_width >= RECTANGLE_WIDTH_CAP:
            self.__rectangle_width = RECTANGLE_WIDTH_CAP
        return self.__rectangle_width

    @property
    def rectangle_x(self):
        self.__rectangle_x = self.width / 2 - (self.rectangle_width / 2)
        return self.__rectangle_x

    @property
    def center(self) -> tuple[int, int]:
        return self.width // 2, self.height // 2

    def pause_text_pos(self, font_width):
        width, height = self.center
        return self.center_window_element(width, font_width), height / 1.6

    @staticmethod
    def center_window_element(width, element_width):
        return width - element_width / 2

    def check_window_size(self) -> bool:
        width, height = self.window.get_size()
        if width != self.width or height != self.height:
            self.height = height
            self.width = width
            return True
        else:
            return False

    @staticmethod
    def set_title():
        display.set_caption("Ringo Mania!")
