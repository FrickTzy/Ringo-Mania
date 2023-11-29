from pygame import display, FULLSCREEN, mouse, RESIZABLE as PYRES, cursors
from Stuff.Ringo_Mania.Frontend.settings import WIDTH, HEIGHT, RESIZABLE, RECTANGLE_X, RECTANGLE_WIDTH, CIRCLE_X_START, \
    BETWEEN_CIRCLE_PADDING, CIRCLE_START_PADDING, CIRCLE_SIZE, \
    RECTANGLE_WIDTH_CAP, LIFE_BAR_COORDINATES, FULL_SCREEN_VIEW, COMBO_Y_PADDING, \
    RECORD_Y_RATIO, NAME_Y_RATIO, \
    RECORD_Y_INTERVAL_RATIO, SCORE_PADDING_RATIO, ACC_Y_RATIO, \
    SCORE_X_RATIO, ACC_X_RATIO


class Display:
    def __init__(self):
        self.width, self.height = WIDTH, HEIGHT
        self.__rectangle_width = RECTANGLE_WIDTH
        self.__circle_x_start = CIRCLE_X_START
        self.__circle_size = CIRCLE_SIZE
        self.__rectangle_x = RECTANGLE_X
        self.__between_circle_padding = BETWEEN_CIRCLE_PADDING
        self.__circle_start_padding = CIRCLE_START_PADDING
        self.__life_bar_coordinates = LIFE_BAR_COORDINATES
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
    def record_y_interval(self):
        return self.height // RECORD_Y_INTERVAL_RATIO

    @property
    def score_padding(self):
        return self.height // SCORE_PADDING_RATIO

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
    def acc_pos_x(self):
        return self.width - (self.height // ACC_X_RATIO)

    @property
    def center(self) -> tuple[int, int]:
        return self.width // 2, self.height // 2

    def pause_text_pos(self, font_width):
        width, height = self.center
        return self.center_window_element(width, font_width), height / 1.6

    @staticmethod
    def center_window_element(width, element_width):
        return width - element_width / 2

    @property
    def record_y(self):
        return self.height // RECORD_Y_RATIO

    @property
    def name_y(self):
        return self.height // NAME_Y_RATIO

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
